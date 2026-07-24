import csv
import html
import io
import json
import os
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

from flask import Flask, Response, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename


APP_DIR = Path(__file__).resolve().parent
load_dotenv(APP_DIR / ".env")

UPLOAD_DIR = APP_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".txt", ".log", ".csv", ".json", ".xml"}
MAX_LOG_CHARS = 60000
MAX_UPLOAD_BYTES = 8 * 1024 * 1024
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-5.4-nano-2026-03-17")
REQUIRED_REPORT_KEYS = {
    "executive_summary",
    "risk_level",
    "risk_rationale",
    "attack_type",
    "affected_assets",
    "indicators_of_compromise",
    "key_findings",
    "timeline",
    "recommended_actions",
}
ATTACK_TYPE_CATEGORIES = [
    "Brute Force",
    "Credential Access",
    "Privilege Escalation",
    "Malware",
    "Reconnaissance",
    "Lateral Movement",
    "Data Exfiltration",
    "Firewall/Network Block",
    "Unknown",
]

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_DIR)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES


def allowed_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def read_uploaded_file(file_storage) -> str:
    if not file_storage or not file_storage.filename:
        return ""

    filename = secure_filename(file_storage.filename)
    if Path(filename).suffix.lower() == ".evtx":
        raise ValueError(
            "Raw .evtx files are not supported in this prototype yet. "
            "Export Windows Event Logs as .xml or .txt before uploading."
        )

    if not allowed_file(filename):
        raise ValueError(
            "Unsupported file type. Use .txt, .log, .csv, .json, or .xml."
        )

    saved_path = UPLOAD_DIR / f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{filename}"
    file_storage.save(saved_path)
    raw_bytes = saved_path.read_bytes()

    for encoding in ("utf-8", "utf-16", "latin-1"):
        try:
            return raw_bytes.decode(encoding)
        except UnicodeDecodeError:
            continue

    return raw_bytes.decode("utf-8", errors="replace")


def infer_event_severity(text: str) -> str:
    lowered = text.lower()
    if any(
        term in lowered
        for term in [
            "critical",
            "malware",
            "ransomware",
            "/etc/shadow",
            "accepted password for root",
        ]
    ):
        return "Critical"
    if any(
        term in lowered
        for term in [
            "sudo",
            "privilege",
            "accepted password",
            "blocked",
            "suspicious",
            "failed password",
        ]
    ):
        return "High"
    if any(term in lowered for term in ["failed", "denied", "warning", "unusual"]):
        return "Medium"
    return "Low"


def normalize_parser_event(record: dict, raw_event: str = "", source: str = "input") -> dict:
    text_for_severity = " ".join(str(value) for value in record.values()) or raw_event
    event_name = record.get("event_type") or record.get("type") or record.get("event")

    return {
        "timestamp": str(record.get("timestamp") or record.get("time") or "Unknown").strip(),
        "source": str(record.get("source") or source or "Unknown").strip(),
        "host": str(record.get("host") or record.get("hostname") or "Unknown").strip(),
        "user": str(record.get("user") or record.get("username") or "Unknown").strip(),
        "source_ip": str(record.get("source_ip") or record.get("src_ip") or record.get("src") or "").strip(),
        "destination_ip": str(
            record.get("destination_ip") or record.get("dst_ip") or record.get("dst") or ""
        ).strip(),
        "event_type": str(event_name or "unknown").strip(),
        "severity": str(record.get("severity") or infer_event_severity(text_for_severity)).strip(),
        "description": str(
            record.get("description") or record.get("message") or record.get("details") or raw_event
        ).strip(),
        "evidence": str(record.get("evidence") or raw_event).strip(),
        "raw_event": str(record.get("raw_event") or raw_event).strip(),
    }


def parse_raw_log_line(line: str) -> dict:
    parsed = {
        "timestamp": "Unknown",
        "source": "raw-log",
        "host": "Unknown",
        "user": "Unknown",
        "source_ip": "",
        "destination_ip": "",
        "event_type": "raw_log_line",
        "severity": infer_event_severity(line),
        "description": line,
        "evidence": line,
        "raw_event": line,
    }

    syslog_match = re.match(
        r"^(?P<timestamp>[A-Z][a-z]{2}\s+\d+\s+\d{2}:\d{2}:\d{2})\s+"
        r"(?P<host>\S+)\s+(?P<process>[^:]+):\s+(?P<message>.*)$",
        line,
    )
    message = line
    if syslog_match:
        parsed["timestamp"] = syslog_match.group("timestamp")
        parsed["host"] = syslog_match.group("host")
        parsed["source"] = f"{syslog_match.group('host')} {syslog_match.group('process')}"
        message = syslog_match.group("message")

    ip_match = re.search(r"\bfrom\s+(\d{1,3}(?:\.\d{1,3}){3})\b", message)
    if ip_match:
        parsed["source_ip"] = ip_match.group(1)

    dst_match = re.search(r"\bDST=(\d{1,3}(?:\.\d{1,3}){3})\b", message)
    if dst_match:
        parsed["destination_ip"] = dst_match.group(1)

    user_match = re.search(r"invalid user\s+(\S+)", message)
    if not user_match:
        user_match = re.search(r"password for\s+(\S+)", message)
    if not user_match:
        user_match = re.search(r"^(\S+)\s*:", message)
    if user_match:
        parsed["user"] = user_match.group(1)

    lowered = message.lower()
    if "failed password" in lowered:
        parsed["event_type"] = "authentication_failure"
        parsed["description"] = "Failed SSH authentication attempt"
    elif "accepted password" in lowered:
        parsed["event_type"] = "authentication_success"
        parsed["description"] = "Successful SSH authentication"
        parsed["severity"] = "Critical" if "root" in lowered else "High"
    elif "command=" in lowered or "sudo" in parsed["source"].lower():
        parsed["event_type"] = "privilege_command"
        parsed["description"] = "Privileged command execution"
        parsed["severity"] = "Critical" if "/etc/shadow" in lowered else "High"
    elif "block" in lowered or "ufw" in parsed["source"].lower():
        parsed["event_type"] = "firewall_block"
        parsed["description"] = "Firewall blocked network traffic"

    return parsed


def parse_input_events(log_text: str) -> list[dict]:
    """Create a lightweight local preview using Zion's canonical event fields."""
    if not log_text.strip():
        return []

    try:
        payload = json.loads(log_text)
        if isinstance(payload, dict) and isinstance(payload.get("events"), list):
            records = payload["events"]
        elif isinstance(payload, list):
            records = payload
        elif isinstance(payload, dict):
            records = [payload]
        else:
            records = []

        return [
            normalize_parser_event(record, json.dumps(record), "json")
            for record in records
            if isinstance(record, dict)
        ]
    except json.JSONDecodeError:
        pass

    first_line = log_text.strip().splitlines()[0] if log_text.strip().splitlines() else ""
    if "," in first_line:
        reader = csv.DictReader(io.StringIO(log_text))
        known_fields = {"timestamp", "time", "source", "host", "user", "event_type", "severity"}
        if reader.fieldnames and known_fields.intersection(set(reader.fieldnames)):
            return [
                normalize_parser_event(row, json.dumps(row), "csv")
                for row in reader
                if any(str(value).strip() for value in row.values())
            ]

    events = []
    for line in [line.strip() for line in log_text.splitlines() if line.strip()][:100]:
        events.append(normalize_parser_event(parse_raw_log_line(line), line, "raw-log"))
    return events


def build_analysis_input(raw_log_text: str, parsed_events: list[dict]) -> str:
    if not parsed_events:
        return raw_log_text

    parser_preview = json.dumps(parsed_events[:50], indent=2)
    return (
        f"{raw_log_text}\n\n"
        "Normalized parser preview using the team event schema. "
        "Use this as supporting context, but cite raw log evidence when possible:\n"
        f"{parser_preview}"
    )


def counter_rows(counter: Counter) -> list[dict]:
    return [
        {"label": name, "count": count}
        for name, count in counter.most_common()
        if name and name != "Unknown"
    ]


def build_timeline_groups(report_timeline: list[dict], parsed_events: list[dict]) -> dict:
    items = []
    if report_timeline:
        items = [
            {
                "severity": item.get("severity", "Unknown"),
                "source": item.get("source", "Unknown"),
                "event": item.get("event", "Unknown"),
            }
            for item in report_timeline
        ]
    elif parsed_events:
        items = [
            {
                "severity": item.get("severity", "Unknown"),
                "source": item.get("source", "Unknown"),
                "event": item.get("event_type", "Unknown"),
            }
            for item in parsed_events
        ]

    return {
        "total_events": len(items),
        "by_severity": counter_rows(Counter(item["severity"] for item in items)),
        "by_source": counter_rows(Counter(item["source"] for item in items)),
        "by_event": counter_rows(Counter(item["event"] for item in items)),
    }


def infer_attack_type_from_text(text: str) -> str:
    lowered = text.lower()
    has_failed_login = "failed password" in lowered or "login_failure" in lowered
    has_successful_root = "accepted password for root" in lowered or "successful login as root" in lowered
    has_sensitive_file = "/etc/shadow" in lowered or "credential" in lowered
    has_sudo = "sudo" in lowered or "privilege" in lowered
    has_firewall_block = "ufw" in lowered or "firewall" in lowered or " block " in lowered
    has_malware = "malware" in lowered or "ransomware" in lowered

    if has_malware:
        return "Malware"
    if has_failed_login and has_successful_root and has_sensitive_file:
        return "Credential Access / Privilege Escalation"
    if has_failed_login and has_successful_root:
        return "Brute Force / Credential Access"
    if has_sudo and has_sensitive_file:
        return "Privilege Escalation / Credential Access"
    if has_sensitive_file:
        return "Credential Access"
    if has_failed_login:
        return "Brute Force"
    if has_firewall_block:
        return "Firewall/Network Block"
    return "Unknown"


def improve_attack_type(current_attack_type: str, source_text: str) -> str:
    inferred = infer_attack_type_from_text(source_text)
    current = (current_attack_type or "Unknown").strip()
    if current.lower() == "unknown":
        return inferred

    lowered = source_text.lower()
    if (
        current == "Credential Access"
        and ("sudo" in lowered or "privilege" in lowered)
        and "/etc/shadow" in lowered
    ):
        return "Credential Access / Privilege Escalation"

    if current == "Brute Force" and "accepted password" in lowered:
        return "Brute Force / Credential Access"

    return current


def infer_risk_level_from_text(text: str) -> str:
    lowered = text.lower()
    if "malware" in lowered or "ransomware" in lowered:
        return "Critical"
    if "accepted password for root" in lowered and "/etc/shadow" in lowered:
        return "Critical"
    if "accepted password for root" in lowered:
        return "Critical"
    if "/etc/shadow" in lowered or "credential" in lowered:
        return "High"
    if "failed password" in lowered and ("block" in lowered or "ufw" in lowered):
        return "High"
    if "failed password" in lowered:
        return "Medium"
    return "Low"


def improve_risk_level(current_risk_level: str, source_text: str) -> str:
    severity_rank = {"Unknown": 0, "Low": 1, "Medium": 2, "High": 3, "Critical": 4}
    current = (current_risk_level or "Unknown").strip().title()
    inferred = infer_risk_level_from_text(source_text)
    return inferred if severity_rank.get(inferred, 0) > severity_rank.get(current, 0) else current


def build_risk_rationale(risk_level: str, source_text: str) -> str:
    lowered = source_text.lower()
    risk = (risk_level or "Unknown").strip()

    if "accepted password for root" in lowered and "/etc/shadow" in lowered:
        return (
            f"Risk is {risk} because the logs show a successful root SSH login followed by access "
            "to /etc/shadow, which indicates possible full system compromise and credential exposure."
        )
    if "accepted password for root" in lowered:
        return (
            f"Risk is {risk} because the logs show successful root authentication over SSH, "
            "which can indicate unauthorized privileged access if not expected."
        )
    if "/etc/shadow" in lowered:
        return (
            f"Risk is {risk} because the logs show access to /etc/shadow, a sensitive credential file."
        )
    if "failed password" in lowered and ("block" in lowered or "ufw" in lowered):
        return (
            f"Risk is {risk} because repeated authentication failures and firewall blocks suggest "
            "active probing or brute-force behavior."
        )
    if "failed password" in lowered:
        return f"Risk is {risk} because the logs show failed authentication attempts."
    return f"Risk is {risk} based on the severity and evidence present in the submitted logs."


def align_risk_language(text: str, risk_level: str) -> str:
    if not text:
        return ""

    risk = (risk_level or "Unknown").strip().title()
    if risk not in {"Low", "Medium", "High", "Critical"}:
        return text

    return re.sub(
        r"\b(risk\s+(?:is|level\s+is|level:)\s+)(Low|Medium|High|Critical)\b",
        lambda match: f"{match.group(1)}{risk}",
        text,
        flags=re.IGNORECASE,
    )


def condense_repeated_timeline_events(timeline: list[dict]) -> list[dict]:
    condensed = []
    seen = {}

    for item in timeline:
        event_key = str(item.get("event", "")).lower()
        details_key = str(item.get("details", "")).lower()
        evidence_key = str(item.get("evidence", "")).lower()
        combined_text = f"{event_key} {details_key} {evidence_key}"

        is_auth_failure = (
            ("failed" in combined_text and ("login" in combined_text or "auth" in combined_text or "password" in combined_text))
            or "auth failure" in combined_text
            or "authentication failure" in combined_text
            or "authentication_failure" in combined_text
            or "failed password" in combined_text
        )

        if is_auth_failure:
            key = (
                item.get("source", "Unknown"),
                item.get("severity", "Unknown"),
                "authentication_failure",
            )
        else:
            condensed.append(item)
            continue

        if key not in seen:
            clone = dict(item)
            clone["_repeat_count"] = 1
            seen[key] = clone
            condensed.append(clone)
            continue

        existing = seen[key]
        existing["_repeat_count"] += 1
        if item.get("evidence") and item["evidence"] not in existing.get("evidence", ""):
            existing["evidence"] = f"{existing.get('evidence', '')}; {item['evidence']}"

    for item in condensed:
        repeat_count = item.pop("_repeat_count", 1)
        if repeat_count > 1:
            item["event"] = "Repeated authentication failures"
            item["details"] = (
                f"{repeat_count} similar authentication failure events were observed from the same source. "
                f"{item.get('details', '')}"
            ).strip()

    return condensed


def improve_report_quality(report: dict, source_text: str) -> dict:
    if not report.get("generated_at"):
        report["generated_at"] = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    report["timeline"] = condense_repeated_timeline_events(report.get("timeline", []))
    report["attack_type"] = improve_attack_type(report.get("attack_type", "Unknown"), source_text)
    report["risk_level"] = improve_risk_level(report.get("risk_level", "Unknown"), source_text)
    report["executive_summary"] = align_risk_language(
        report.get("executive_summary", ""),
        report["risk_level"],
    )
    if not report.get("risk_rationale"):
        report["risk_rationale"] = build_risk_rationale(report["risk_level"], source_text)
    else:
        report["risk_rationale"] = align_risk_language(report["risk_rationale"], report["risk_level"])

    if report.get("recommended_actions") and len(report["recommended_actions"]) < 3:
        report["recommended_actions"].append(
            "Continue reviewing surrounding authentication, sudo, and firewall logs to confirm scope and identify any persistence."
        )

    return report


def build_prompt(log_text: str) -> str:
    return f"""
You are a cybersecurity analyst helping a student capstone team.
Analyze the security logs below and produce a concise threat report.

Return ONLY valid JSON with this exact shape:
{{
  "executive_summary": "2-4 sentence plain-English summary that states what happened, what asset or account was affected, and why it matters",
  "risk_level": "Low | Medium | High | Critical",
  "risk_rationale": "1-2 sentences explaining why this risk level was selected using evidence from the logs",
  "attack_type": "best-fit attack category or Unknown",
  "affected_assets": [
    "hostnames, usernames, IP addresses, systems, or files affected"
  ],
  "indicators_of_compromise": [
    "suspicious IPs, accounts, file paths, commands, hashes, domains, or event IDs"
  ],
  "key_findings": [
    "finding 1",
    "finding 2"
  ],
  "timeline": [
    {{
      "timestamp": "timestamp from logs or Unknown",
      "source": "host, account, IP, process, or log source",
      "event": "short event title",
      "severity": "Low | Medium | High | Critical",
      "details": "what happened and why it matters",
      "evidence": "specific log line, event ID, IP, user, command, or artifact supporting this event"
    }}
  ],
  "recommended_actions": [
    "action 1",
    "action 2"
  ]
}}

Rules:
- Do not invent facts not supported by the logs.
- If timestamps are missing, order events by appearance and use "Unknown".
- If a required top-level field has no supported value, use "Unknown" for strings
  or an empty list for arrays.
- Use a specific attack_type when evidence supports it. Preferred categories:
  Brute Force, Credential Access, Privilege Escalation, Malware,
  Reconnaissance, Lateral Movement, Data Exfiltration, Firewall/Network Block,
  or a clear combination such as "Brute Force / Credential Access".
  Use "Unknown" only when the logs do not support a meaningful category.
- The executive_summary should explain the likely incident in plain English:
  who or what was involved, what happened, what the impact is, and why the risk
  level was chosen.
- The risk_rationale should briefly explain the risk level using concrete log
  evidence such as successful root login, sensitive file access, malware
  indicators, repeated failed logins, or firewall blocks.
- The executive_summary, risk_level, and risk_rationale must not contradict
  each other.
- Key findings should be 3-5 concise bullets supported by the logs.
- Recommended actions should be 3-5 prioritized analyst actions, starting with
  the most urgent containment, credential, or evidence-preservation step.
- Consistency rules for the report summary:
  - Use the same severity meaning across all log samples:
    Low = informational or blocked activity with no compromise,
    Medium = suspicious activity without confirmed compromise,
    High = likely attack activity or repeated suspicious behavior,
    Critical = confirmed compromise, privileged access, malware execution,
    sensitive file access, or likely data exposure.
  - Keep executive_summary wording consistent across tests: start with the
    affected system or account, describe the main event sequence, then explain
    the impact and risk level.
  - Do not say the risk is one level in the executive_summary and a different
    level in risk_level or risk_rationale.
  - Use consistent attack_type names across similar logs. For example, repeated
    failed SSH logins should be "Brute Force", successful root access should
    include "Credential Access", sudo misuse should include "Privilege Escalation",
    and suspicious encryption or malware alerts should include "Malware".
  - Keep key findings and recommended actions aligned with the same incident
    narrative used in the executive_summary.
- Rules for the Threat Timeline:
  - Create a chronological threat timeline of the most important security events.
  - Every timeline event must include: timestamp, source, event, severity,
    details, and evidence.
  - Make event titles short, clear, and descriptive (avoid long repetitive titles).
  - Combine repeated similar events when possible (for example, multiple failed
    login attempts from the same IP can be summarized into one event instead of
    creating many duplicate entries).
  - In the "details" field, explain what happened and why it matters in 1-2
    sentences.
  - In the "evidence" field, always cite the specific log line, command, IP
    address, username, or artifact that supports the event.
  - Use severity levels: Low, Medium, High, or Critical appropriately.
  - Focus on high-impact events such as successful logins after failures,
    privilege escalation (sudo), sensitive file access, and firewall blocks.
  - Do not invent events that are not supported by the logs.
  - Keep the timeline concise but useful for incident response review.
- Identify affected assets and indicators of compromise only when supported by
  the logs. Use an empty list when none are present.
- For timeline evidence, cite specific log details instead of broad summaries.
- Use "Unknown" for attack_type when the logs do not support a clear category.
- Keep the report useful for an incident-response timeline.

Logs:
{log_text}
""".strip()


def parse_model_json(output_text: str) -> dict:
    cleaned = output_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```json").removeprefix("```").strip()
        cleaned = cleaned.removesuffix("```").strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(cleaned[start : end + 1])
            except json.JSONDecodeError:
                pass
        raise


def normalize_text_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def normalize_timeline_item(item) -> dict:
    if not isinstance(item, dict):
        return {
            "timestamp": "Unknown",
            "source": "Unknown",
            "event": str(item).strip() or "Unknown event",
            "severity": "Unknown",
            "details": "",
            "evidence": "",
        }

    return {
        "timestamp": str(item.get("timestamp") or "Unknown").strip(),
        "source": str(item.get("source") or "Unknown").strip(),
        "event": str(item.get("event") or "Unknown event").strip(),
        "severity": str(item.get("severity") or "Unknown").strip(),
        "details": str(item.get("details") or "").strip(),
        "evidence": str(item.get("evidence") or "").strip(),
    }


def normalize_report(report: dict) -> dict:
    if not isinstance(report, dict):
        report = {"executive_summary": str(report)}

    normalized = empty_report()
    normalized["executive_summary"] = str(
        report.get("executive_summary") or ""
    ).strip()
    normalized["generated_at"] = str(report.get("generated_at") or "").strip()
    normalized["risk_level"] = str(report.get("risk_level") or "Unknown").strip()
    normalized["risk_rationale"] = str(report.get("risk_rationale") or "").strip()
    normalized["attack_type"] = str(report.get("attack_type") or "Unknown").strip()
    normalized["affected_assets"] = normalize_text_list(report.get("affected_assets"))
    normalized["indicators_of_compromise"] = normalize_text_list(
        report.get("indicators_of_compromise")
    )
    normalized["key_findings"] = normalize_text_list(report.get("key_findings"))
    normalized["recommended_actions"] = normalize_text_list(
        report.get("recommended_actions")
    )

    timeline = report.get("timeline")
    normalized["timeline"] = (
        [normalize_timeline_item(item) for item in timeline]
        if isinstance(timeline, list)
        else []
    )

    missing_keys = sorted(REQUIRED_REPORT_KEYS - set(report.keys()))
    if missing_keys:
        normalized["recommended_actions"].append(
            f"Review output: missing expected field(s): {', '.join(missing_keys)}."
        )

    return normalized


def analyze_logs_with_openai(log_text: str) -> dict:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set.")

    trimmed_log_text = log_text[:MAX_LOG_CHARS]
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a cybersecurity analyst helping a student capstone team.",
            },
            {"role": "user", "content": build_prompt(trimmed_log_text)},
        ],
        max_completion_tokens=2000,
        response_format={"type": "json_object"},
        temperature=0.3,
    )

    output_text = (response.choices[0].message.content or "").strip()
    try:
        return improve_report_quality(
            normalize_report(parse_model_json(output_text)),
            trimmed_log_text,
        )
    except json.JSONDecodeError:
        return improve_report_quality(
            normalize_report(
                {
                    "executive_summary": output_text,
                    "risk_level": "Unknown",
                    "risk_rationale": "",
                    "attack_type": "Unknown",
                    "affected_assets": [],
                    "indicators_of_compromise": [],
                    "key_findings": [],
                    "timeline": [],
                    "recommended_actions": [
                        "Review the raw model output because it was not valid JSON."
                    ],
                }
            ),
            trimmed_log_text,
        )


def empty_report() -> dict:
    return {
        "executive_summary": "",
        "generated_at": "",
        "risk_level": "",
        "risk_rationale": "",
        "attack_type": "",
        "affected_assets": [],
        "indicators_of_compromise": [],
        "key_findings": [],
        "timeline": [],
        "recommended_actions": [],
    }


def build_downloadable_report_html(report: dict) -> str:
    def esc(value) -> str:
        return html.escape(str(value or ""))

    def list_items(values: list[str]) -> str:
        if not values:
            return '<p class="empty">No items returned.</p>'
        return "<ul>" + "".join(f"<li>{esc(value)}</li>" for value in values) + "</ul>"

    def count_items(counter: Counter) -> str:
        rows = [
            f"<li><strong>{esc(name)}:</strong> {count}</li>"
            for name, count in counter.most_common()
            if name and name != "Unknown"
        ]
        if not rows:
            return '<p class="empty">No grouped counts returned.</p>'
        return "<ul>" + "".join(rows) + "</ul>"

    def severity_class(value) -> str:
        severity = str(value or "").strip().lower()
        if severity in {"low", "medium", "high", "critical"}:
            return severity
        return "unknown"

    timeline = report.get("timeline", [])
    high_critical_count = sum(
        1
        for item in timeline
        if str(item.get("severity", "")).strip().lower() in {"high", "critical"}
    )
    severity_counts = Counter(str(item.get("severity", "Unknown")).strip() for item in timeline)
    event_counts = Counter(str(item.get("event", "Unknown")).strip() for item in timeline)

    timeline_items = []
    for item in timeline:
        severity = esc(item.get("severity", "Unknown"))
        timeline_items.append(
            f"""
            <article class="event">
              <div class="event-meta">
                <span>{esc(item.get("timestamp", "Unknown"))}</span>
                <span>{esc(item.get("source", "Unknown"))}</span>
                <span class="badge {severity_class(severity)}">{severity}</span>
              </div>
              <h3>{esc(item.get("event", "Unknown event"))}</h3>
              <p>{esc(item.get("details", ""))}</p>
              <p class="evidence"><strong>Evidence:</strong> {esc(item.get("evidence", ""))}</p>
            </article>
            """
        )

    timeline_html = "\n".join(timeline_items) or '<p class="empty">No timeline events returned.</p>'
    risk_level = esc(report.get("risk_level", "Unknown"))

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Security Log Threat Report</title>
  <style>
    :root {{
      --bg: #eef2f6;
      --surface: #ffffff;
      --ink: #111827;
      --muted: #53627a;
      --line: #d7e0ea;
      --brand: #142136;
      --accent: #0f766e;
      --low: #4b5563;
      --medium: #b7791f;
      --high: #c05621;
      --critical: #b91c1c;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Arial, Helvetica, sans-serif;
      line-height: 1.55;
    }}
    header {{
      background: var(--brand);
      color: #ffffff;
      padding: 32px 44px;
    }}
    header h1 {{ margin: 0 0 8px; font-size: 2rem; }}
    header p {{ margin: 0; max-width: 900px; }}
    main {{ max-width: 1180px; margin: 28px auto; padding: 0 22px 42px; }}
    section.panel {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 14px 36px rgba(17, 24, 39, 0.06);
      margin: 18px 0;
      padding: 24px;
    }}
    h2 {{ margin-top: 0; color: #0f172a; }}
    .summary-grid {{
      display: grid;
      grid-template-columns: 1fr 220px;
      gap: 22px;
      align-items: start;
    }}
    .risk-card {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
      text-align: center;
      background: #f8fafc;
    }}
    .risk-card .label {{
      color: var(--muted);
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }}
    .risk-card .risk {{
      color: var(--critical);
      display: block;
      font-size: 1.55rem;
      font-weight: 800;
      margin-top: 8px;
    }}
    .metric-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
      margin-top: 18px;
    }}
    .metric {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      background: #fbfdff;
    }}
    .metric span {{
      color: var(--muted);
      display: block;
      font-size: 0.78rem;
      font-weight: 700;
      margin-bottom: 6px;
      text-transform: uppercase;
    }}
    .metric strong {{ font-size: 1.25rem; }}
    .two-col {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 18px;
    }}
    .subcard {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      background: #fbfdff;
    }}
    .event {{
      border-left: 4px solid var(--accent);
      border-radius: 4px;
      padding: 14px 18px;
      margin: 14px 0;
      background: #f8fafc;
    }}
    .event h3 {{ margin: 8px 0; }}
    .event-meta {{
      align-items: center;
      color: var(--muted);
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      font-size: 0.92rem;
    }}
    .evidence {{ color: #475569; font-size: 0.94rem; }}
    .badge {{
      border-radius: 999px;
      color: #ffffff;
      display: inline-block;
      font-size: 0.78rem;
      font-weight: 700;
      padding: 3px 10px;
    }}
    .badge.low {{ background: var(--low); }}
    .badge.medium {{ background: var(--medium); }}
    .badge.high {{ background: var(--high); }}
    .badge.critical {{ background: var(--critical); }}
    .badge.unknown {{ background: #64748b; }}
    .empty {{ color: var(--muted); }}
    ul {{ padding-left: 22px; }}
    li {{ margin: 4px 0; }}
    @media (max-width: 800px) {{
      header {{ padding: 24px; }}
      .summary-grid, .two-col, .metric-grid {{ grid-template-columns: 1fr; }}
      main {{ padding: 0 14px 28px; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Intelligent Security Log Summarization</h1>
    <p>Saved HTML threat report with summary, risk scoring, timeline events, evidence, and recommended actions.</p>
  </header>
  <main>
  <section class="panel">
    <div class="summary-grid">
      <div>
        <h2>Report Summary</h2>
        <p>{esc(report.get("executive_summary", ""))}</p>
        <div class="metric-grid">
          <div class="metric"><span>Generated</span><strong>{esc(report.get("generated_at", "Unknown"))}</strong></div>
          <div class="metric"><span>Attack Type</span><strong>{esc(report.get("attack_type", "Unknown"))}</strong></div>
          <div class="metric"><span>High/Critical</span><strong>{high_critical_count}</strong></div>
        </div>
        <p><strong>Risk Rationale:</strong> {esc(report.get("risk_rationale", ""))}</p>
      </div>
      <aside class="risk-card">
        <span class="label">Overall Risk</span>
        <span class="risk">{risk_level}</span>
      </aside>
    </div>
  </section>

  <section class="panel">
    <h2>Assets and Indicators</h2>
    <div class="two-col">
      <div class="subcard">
        <h3>Affected Assets</h3>
        {list_items(report.get("affected_assets", []))}
      </div>
      <div class="subcard">
        <h3>Indicators of Compromise</h3>
        {list_items(report.get("indicators_of_compromise", []))}
      </div>
    </div>
  </section>

  <section class="panel">
    <h2>Timeline Groups</h2>
    <div class="two-col">
      <div class="subcard">
        <h3>Severity Counts</h3>
        {count_items(severity_counts)}
      </div>
      <div class="subcard">
        <h3>Event Counts</h3>
        {count_items(event_counts)}
      </div>
    </div>
  </section>

  <section class="panel">
    <h2>Key Findings</h2>
    {list_items(report.get("key_findings", []))}
  </section>

  <section class="panel">
    <h2>Threat Timeline</h2>
    {timeline_html}
  </section>

  <section class="panel">
    <h2>Recommended Actions</h2>
    {list_items(report.get("recommended_actions", []))}
  </section>

  <section class="panel">
    <h2>Known Limitations</h2>
    <ul>
      <li>This prototype summarizes the uploaded log evidence and does not verify indicators against live threat intelligence feeds.</li>
      <li>Raw EVTX parsing is not included; Windows Event Logs should be exported as text or XML before upload.</li>
      <li>Analysts should validate the timeline against original log sources before taking final incident-response action.</li>
    </ul>
  </section>
  </main>
</body>
</html>
"""


@app.route("/download-report", methods=["POST"])
def download_report():
    try:
        report = normalize_report(json.loads(request.form.get("report_json", "{}")))
    except json.JSONDecodeError:
        report = empty_report()

    file_format = request.form.get("format", "json")
    if file_format == "html":
        return Response(
            build_downloadable_report_html(report),
            mimetype="text/html",
            headers={"Content-Disposition": "attachment; filename=security_log_report.html"},
        )

    return Response(
        json.dumps(report, indent=2),
        mimetype="application/json",
        headers={"Content-Disposition": "attachment; filename=security_log_report.json"},
    )


@app.route("/", methods=["GET", "POST"])
def index():
    report = empty_report()
    error = None
    submitted_log_text = ""
    parsed_events = []
    timeline_groups = build_timeline_groups([], [])

    if request.method == "POST":
        try:
            pasted_logs = request.form.get("log_text", "").strip()
            uploaded_logs = read_uploaded_file(request.files.get("log_file"))
            submitted_log_text = "\n\n".join(
                part for part in [pasted_logs, uploaded_logs] if part
            ).strip()

            if not submitted_log_text:
                raise ValueError("Paste logs or upload a log file before analyzing.")

            parsed_events = parse_input_events(submitted_log_text)
            report = analyze_logs_with_openai(
                build_analysis_input(submitted_log_text, parsed_events)
            )
            timeline_groups = build_timeline_groups(report["timeline"], parsed_events)
        except Exception as exc:
            error = str(exc)
            submitted_log_text = request.form.get("log_text", "")
            parsed_events = parse_input_events(submitted_log_text)
            timeline_groups = build_timeline_groups([], parsed_events)

    return render_template(
        "index.html",
        report=report,
        error=error,
        log_text=submitted_log_text,
        parsed_events=parsed_events[:10],
        timeline_groups=timeline_groups,
        model_name=MODEL_NAME,
        max_chars=MAX_LOG_CHARS,
    )


@app.errorhandler(RequestEntityTooLarge)
def handle_large_upload(_error):
    report = empty_report()
    return (
        render_template(
            "index.html",
            report=report,
            error="Uploaded file is too large. Use a file smaller than 8 MB.",
            log_text=request.form.get("log_text", ""),
            parsed_events=[],
            timeline_groups=build_timeline_groups([], []),
            model_name=MODEL_NAME,
            max_chars=MAX_LOG_CHARS,
        ),
        413,
    )


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=debug_mode)
