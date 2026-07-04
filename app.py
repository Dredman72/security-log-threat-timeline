import json
import os
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


def build_prompt(log_text: str) -> str:
    return f"""
You are a cybersecurity analyst helping a student capstone team.
Analyze the security logs below and produce a concise threat report.

Return ONLY valid JSON with this exact shape:
{{
  "executive_summary": "2-4 sentence plain-English summary",
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
        return normalize_report(parse_model_json(output_text))
    except json.JSONDecodeError:
        return normalize_report(
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

    if request.method == "POST":
        try:
            pasted_logs = request.form.get("log_text", "").strip()
            uploaded_logs = read_uploaded_file(request.files.get("log_file"))
            submitted_log_text = "\n\n".join(
                part for part in [pasted_logs, uploaded_logs] if part
            ).strip()

            if not submitted_log_text:
                raise ValueError("Paste logs or upload a log file before analyzing.")

            report = analyze_logs_with_openai(submitted_log_text)
        except Exception as exc:
            error = str(exc)
            submitted_log_text = request.form.get("log_text", "")

    return render_template(
        "index.html",
        report=report,
        error=error,
        log_text=submitted_log_text,
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
            model_name=MODEL_NAME,
            max_chars=MAX_LOG_CHARS,
        ),
        413,
    )


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=debug_mode)
