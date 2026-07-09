import csv
import io
import json
import os
from collections import Counter
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request
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
        events.append(
            normalize_parser_event(
                {
                    "timestamp": "Unknown",
                    "source": "raw-log",
                    "event_type": "raw_log_line",
                    "severity": infer_event_severity(line),
                    "description": line,
                    "evidence": line,
                    "raw_event": line,
                },
                line,
                "raw-log",
            )
        )
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
        {"name": name, "count": count}
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


def condense_repeated_timeline_events(timeline: list[dict]) -> list[dict]:
    condensed = []
    seen = {}

    for item in timeline:
        event_key = str(item.get("event", "")).lower()
        if "failed" in event_key and "login" in event_key:
            key = (
                item.get("source", "Unknown"),
                item.get("severity", "Unknown"),
                "failed_login",
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
            existing["evidence"] = f"{existing.get('evidence', '')} | {item['evidence']}"

    for item in condensed:
        repeat_count = item.pop("_repeat_count", 1)
        if repeat_count > 1:
            item["event"] = "Repeated failed login attempts"
            item["details"] = (
                f"{repeat_count} similar failed login events were observed from the same source. "
                f"{item.get('details', '')}"
            ).strip()

    return condensed


def improve_report_quality(report: dict, source_text: str) -> dict:
    report["timeline"] = condense_repeated_timeline_events(report.get("timeline", []))

    if not report.get("attack_type") or report["attack_type"].lower() == "unknown":
        report["attack_type"] = infer_attack_type_from_text(source_text)

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
- Key findings should be 3-5 concise bullets supported by the logs.
- Recommended actions should be 3-5 prioritized analyst actions, starting with
  the most urgent containment, credential, or evidence-preservation step.
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
    normalized["risk_level"] = str(report.get("risk_level") or "Unknown").strip()
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
        "risk_level": "",
        "attack_type": "",
        "affected_assets": [],
        "indicators_of_compromise": [],
        "key_findings": [],
        "timeline": [],
        "recommended_actions": [],
    }


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
