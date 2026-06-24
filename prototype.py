"""
Intelligent Security Log Summarization and Threat Timeline prototype.

Zion's backend focus:
- ingest security log files
- parse records into one canonical event schema
- validate malformed or unsupported input
- pass normalized events to the summarization layer
- generate a basic report artifact for the frontend/report workflow

No model training is required. The prototype runs in demo mode until the
instructor-provided OpenAI API key is added to .env.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_MODEL = "gpt-5.4-mini"
DEFAULT_PROJECT_NAME = "Intelligent Security Log Summarization"
ALLOWED_SEVERITIES = {"Low", "Medium", "High", "Critical"}


@dataclass(frozen=True)
class PrototypeConfig:
    project_name: str
    openai_api_key: str | None
    model: str
    data_dir: Path
    report_dir: Path


@dataclass(frozen=True)
class SecurityEvent:
    timestamp: str
    source: str
    host: str
    user: str
    event_type: str
    severity: str
    description: str
    evidence: str
    raw_event: str


def load_dotenv_if_available() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return

    load_dotenv()


def load_config() -> PrototypeConfig:
    load_dotenv_if_available()

    return PrototypeConfig(
        project_name=os.getenv("PROJECT_NAME", DEFAULT_PROJECT_NAME),
        openai_api_key=os.getenv("OPENAI_API_KEY") or None,
        model=os.getenv("OPENAI_MODEL", DEFAULT_MODEL),
        data_dir=Path(os.getenv("PROTOTYPE_DATA_DIR", "data")),
        report_dir=Path(os.getenv("PROTOTYPE_REPORT_DIR", "reports")),
    )


def infer_severity(text: str) -> str:
    lowered = text.lower()
    if any(term in lowered for term in ["critical", "malware", "ransomware"]):
        return "Critical"
    if any(term in lowered for term in ["failed", "denied", "blocked", "suspicious"]):
        return "High"
    if any(term in lowered for term in ["warning", "scan", "unusual"]):
        return "Medium"
    return "Low"


def normalize_event(record: dict[str, Any], raw_event: str, source: str) -> SecurityEvent:
    """Convert a parsed record into the team's canonical event schema."""
    description = str(
        record.get("description")
        or record.get("message")
        or record.get("event")
        or record.get("details")
        or raw_event
    )

    return SecurityEvent(
        timestamp=str(record.get("timestamp") or record.get("time") or "unknown"),
        source=str(record.get("source") or source),
        host=str(record.get("host") or record.get("hostname") or "unknown"),
        user=str(record.get("user") or record.get("username") or "unknown"),
        event_type=str(record.get("event_type") or record.get("type") or "unknown"),
        severity=str(record.get("severity") or infer_severity(description)),
        description=description,
        evidence=str(record.get("evidence") or raw_event),
        raw_event=raw_event,
    )


def parse_json_log(path: Path) -> list[SecurityEvent]:
    events: list[SecurityEvent] = []
    content = path.read_text(encoding="utf-8")
    payload = json.loads(content)
    records = payload if isinstance(payload, list) else [payload]

    for record in records:
        if isinstance(record, dict):
            events.append(normalize_event(record, json.dumps(record), path.name))

    return events


def parse_csv_log(path: Path) -> list[SecurityEvent]:
    events: list[SecurityEvent] = []
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError("CSV file is missing a header row.")

        for record in reader:
            if None in record:
                raise ValueError(
                    "CSV row has more values than headers. Check for malformed commas."
                )
            events.append(normalize_event(record, json.dumps(record), path.name))
    return events


def parse_text_log(path: Path) -> list[SecurityEvent]:
    events: list[SecurityEvent] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        cleaned = line.strip()
        if not cleaned:
            continue
        record = {
            "timestamp": "unknown",
            "source": path.name,
            "event_type": "text_log_line",
            "description": cleaned,
            "evidence": f"line {line_number}: {cleaned}",
        }
        events.append(normalize_event(record, cleaned, path.name))
    return events


def parse_log_file(path: Path) -> list[SecurityEvent]:
    """Parse supported log files into canonical security events."""
    # TODO Milestone 3, Zion: Add real parsers for the selected first log type,
    # such as Sysmon CSV/XML, Windows Event Log exports, firewall CSV, or EDR logs.
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")
    if path.stat().st_size == 0:
        raise ValueError(f"Log file is empty: {path}")

    suffix = path.suffix.lower()
    if suffix == ".json":
        return parse_json_log(path)
    if suffix == ".csv":
        return parse_csv_log(path)
    if suffix in {".txt", ".log"}:
        return parse_text_log(path)

    raise ValueError(f"Unsupported log type: {suffix or 'no extension'}")


def validate_events(events: list[SecurityEvent]) -> list[str]:
    """Return validation warnings for parser output."""
    warnings: list[str] = []
    if not events:
        warnings.append("No events were parsed from the input file.")

    missing_timestamps = sum(1 for event in events if event.timestamp == "unknown")
    if missing_timestamps:
        warnings.append(f"{missing_timestamps} event(s) are missing timestamps.")

    missing_descriptions = sum(
        1 for event in events if not event.description or event.description == "unknown"
    )
    if missing_descriptions:
        warnings.append(f"{missing_descriptions} event(s) are missing descriptions.")

    bad_severities = sorted(
        {event.severity for event in events if event.severity not in ALLOWED_SEVERITIES}
    )
    if bad_severities:
        warnings.append(
            "Unexpected severity value(s): " + ", ".join(bad_severities)
        )

    unknown_event_types = sum(1 for event in events if event.event_type == "unknown")
    if unknown_event_types:
        warnings.append(f"{unknown_event_types} event(s) have unknown event types.")

    return warnings


def build_prompt(events: list[SecurityEvent]) -> str:
    """Create the prompt sent to the OpenAI API."""
    event_payload = [asdict(event) for event in events[:50]]
    return (
        "You are helping security analysts review normalized security events.\n"
        "Return concise, professional JSON with these exact top-level keys:\n"
        "- executive_summary: string\n"
        "- key_findings: array of strings\n"
        "- timeline_events: array of objects with timestamp, severity, title, details\n"
        "- indicators: array of strings\n"
        "- recommendations: array of strings\n\n"
        "Focus on security analyst usefulness. Do not invent facts that are not "
        "supported by the events. If evidence is limited, say so clearly.\n\n"
        f"Normalized events:\n{json.dumps(event_payload, indent=2)}"
    )


def build_local_summary_payload(
    events: list[SecurityEvent], warnings: list[str]
) -> dict[str, Any]:
    """Create structured demo output when no API key is configured."""
    high_or_worse = [
        event for event in events if event.severity.lower() in {"high", "critical"}
    ]
    timeline_events = [
        {
            "timestamp": event.timestamp,
            "severity": event.severity,
            "title": event.event_type,
            "details": event.description,
        }
        for event in generate_timeline(events)
    ]
    return {
        "executive_summary": (
            "Demo summary: backend parsing and structured AI handoff are working. "
            f"The parser produced {len(events)} normalized events, including "
            f"{len(high_or_worse)} High/Critical events."
        ),
        "key_findings": [
            f"Parsed events: {len(events)}",
            f"High/Critical events: {len(high_or_worse)}",
            "OpenAI API summaries will be enabled after the API key is configured.",
        ],
        "timeline_events": timeline_events,
        "indicators": [
            event.evidence
            for event in high_or_worse
            if event.evidence and event.evidence != "unknown"
        ],
        "recommendations": [
            "Review High and Critical events first.",
            "Confirm whether suspicious activity is expected or unauthorized.",
            "Preserve raw log evidence for incident review.",
        ],
        "validation_warnings": warnings,
    }


def format_summary_payload(payload: dict[str, Any]) -> str:
    lines = [payload.get("executive_summary", "No executive summary available.")]
    findings = payload.get("key_findings") or []
    if findings:
        lines.append("")
        lines.append("Key findings:")
        lines.extend(f"- {item}" for item in findings)
    recommendations = payload.get("recommendations") or []
    if recommendations:
        lines.append("")
        lines.append("Recommendations:")
        lines.extend(f"- {item}" for item in recommendations)
    warnings = payload.get("validation_warnings") or []
    if warnings:
        lines.append("")
        lines.append("Validation warnings:")
        lines.extend(f"- {item}" for item in warnings)
    return "\n".join(lines)


def local_demo_summary(events: list[SecurityEvent], warnings: list[str]) -> str:
    payload = build_local_summary_payload(events, warnings)
    return format_summary_payload(payload)


def summarize_events(
    config: PrototypeConfig,
    events: list[SecurityEvent],
    warnings: list[str],
) -> str:
    if not config.openai_api_key:
        return local_demo_summary(events, warnings)

    try:
        from openai import OpenAI
    except ImportError:
        return "OpenAI package is not installed. Install prerequisites from README.md."

    client = OpenAI(api_key=config.openai_api_key)
    response = client.responses.create(
        model=config.model,
        input=build_prompt(events),
    )
    if not response.output_text:
        return local_demo_summary(events, warnings)
    return response.output_text


def generate_timeline(events: list[SecurityEvent]) -> list[SecurityEvent]:
    """Return events ordered for timeline display."""
    # TODO Milestone 5, Zion and Oriah: Add grouping by host, user, process, IP,
    # event type, and severity for the interactive timeline.
    return sorted(events, key=lambda event: event.timestamp)


def write_html_report(
    config: PrototypeConfig,
    events: list[SecurityEvent],
    warnings: list[str],
    summary: str,
) -> Path:
    """Generate a simple HTML report for the frontend/report milestone."""
    # TODO Milestone 6, Oriah and Zion: Replace this starter HTML with the final
    # interactive timeline and polished report layout.
    config.report_dir.mkdir(parents=True, exist_ok=True)
    report_path = config.report_dir / "security_report.html"
    timeline_rows = "\n".join(
        "<tr>"
        f"<td>{html.escape(event.timestamp)}</td>"
        f"<td>{html.escape(event.severity)}</td>"
        f"<td>{html.escape(event.host)}</td>"
        f"<td>{html.escape(event.user)}</td>"
        f"<td>{html.escape(event.event_type)}</td>"
        f"<td>{html.escape(event.description)}</td>"
        "</tr>"
        for event in generate_timeline(events)
    )
    warning_items = "\n".join(f"<li>{html.escape(item)}</li>" for item in warnings)

    report_path.write_text(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{html.escape(config.project_name)}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; line-height: 1.45; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 1rem; }}
    th, td {{ border: 1px solid #ccc; padding: 0.5rem; text-align: left; }}
    th {{ background: #f1f3f5; }}
    pre {{ background: #f7f7f7; padding: 1rem; white-space: pre-wrap; }}
  </style>
</head>
<body>
  <h1>{html.escape(config.project_name)}</h1>
  <h2>Executive Summary</h2>
  <pre>{html.escape(summary)}</pre>
  <h2>Validation Warnings</h2>
  <ul>{warning_items or "<li>No validation warnings.</li>"}</ul>
  <h2>Threat Timeline</h2>
  <table>
    <thead>
      <tr>
        <th>Timestamp</th>
        <th>Severity</th>
        <th>Host</th>
        <th>User</th>
        <th>Type</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>{timeline_rows}</tbody>
  </table>
</body>
</html>
""",
        encoding="utf-8",
    )
    return report_path


def save_events(config: PrototypeConfig, events: list[SecurityEvent]) -> Path:
    config.data_dir.mkdir(parents=True, exist_ok=True)
    output_path = config.data_dir / "normalized_events.json"
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "events": [asdict(event) for event in events],
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output_path


def demo_events() -> list[SecurityEvent]:
    return [
        normalize_event(
            {
                "timestamp": "2026-06-09T13:00:00Z",
                "source": "demo-sysmon",
                "host": "WIN-SERVER-01",
                "user": "alice",
                "event_type": "process_start",
                "description": "PowerShell launched with unusual encoded command.",
                "severity": "High",
            },
            "PowerShell launched with unusual encoded command.",
            "demo",
        ),
        normalize_event(
            {
                "timestamp": "2026-06-09T13:05:00Z",
                "source": "demo-firewall",
                "host": "WIN-SERVER-01",
                "user": "unknown",
                "event_type": "network_connection",
                "description": "Outbound connection blocked to suspicious IP.",
                "severity": "High",
            },
            "Outbound connection blocked to suspicious IP.",
            "demo",
        ),
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the security log prototype.")
    parser.add_argument("--log-file", help="Path to a CSV, JSON, TXT, or LOG file.")
    parser.add_argument("--health", action="store_true", help="Print deployment status.")
    parser.add_argument("--no-save", action="store_true", help="Skip writing output files.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config()

    if args.health:
        print(
            json.dumps(
                {
                    "status": "ok",
                    "project_name": config.project_name,
                    "model": config.model,
                    "api_key_configured": bool(config.openai_api_key),
                    "supported_log_types": [".csv", ".json", ".txt", ".log"],
                },
                indent=2,
            )
        )
        return

    if args.log_file:
        events = parse_log_file(Path(args.log_file))
    else:
        events = demo_events()

    warnings = validate_events(events)
    summary = summarize_events(config, events, warnings)

    print(config.project_name)
    print("=" * len(config.project_name))
    print(summary)

    if not args.no_save:
        events_path = save_events(config, events)
        report_path = write_html_report(config, events, warnings, summary)
        print()
        print(f"Normalized events saved to: {events_path}")
        print(f"HTML report saved to: {report_path}")

    # TODO Milestone 7, entire team: Add tests, final README, demo dataset,
    # presentation visuals, and deployment notes for Windows Server 2025 and
    # Ubuntu 24.04 LTS.


if __name__ == "__main__":
    main()
