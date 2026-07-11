# Week 6: Report Data Fields

## Purpose

This document defines the backend/report-ready data fields needed by the Week 6 HTML report generator.

The frontend should expect one report-ready JSON object with these sections:

- `report_summary`
- `risk_level`
- `key_findings`
- `timeline_events`
- `assets_and_indicators`
- `recommended_actions`
- `raw_event_details`
- `known_limitations`

## Report Summary

| Field | Description |
|---|---|
| `executive_summary` | Short summary of the security activity found in the uploaded log file. |
| `generated_at` | Timestamp when the report data was generated. |
| `input_file` | Name of the uploaded source file. |
| `total_events` | Total number of parsed events. |
| `high_or_critical_events` | Count of high or critical severity events. |

## Risk Level

| Field | Description |
|---|---|
| `overall_risk` | Overall report risk rating, such as Low, Medium, High, or Critical. |
| `severity_counts` | Count of events by severity level. |
| `highest_severity` | Highest severity found in the parsed events. |
| `risk_reason` | Short explanation for the overall risk rating. |

## Key Findings

Each finding should include:

| Field | Description |
|---|---|
| `title` | Short finding title. |
| `severity` | Severity of the finding. |
| `description` | Explanation of the finding. |
| `supporting_event_ids` | Related timeline event IDs. |

## Timeline Events

Each timeline event should include:

| Field | Description |
|---|---|
| `event_id` | Unique event identifier. |
| `timestamp` | Time the event occurred. |
| `source` | Log source, such as firewall, EDR, auth, or sysmon. |
| `host` | Hostname involved in the event. |
| `user` | User account involved, if available. |
| `source_ip` | Source IP address, if available. |
| `destination_ip` | Destination IP address, if available. |
| `event_type` | Standardized event type. |
| `severity` | Event severity. |
| `description` | Human-readable event description. |
| `evidence` | Supporting evidence from the log. |
| `raw_event` | Original raw log line or raw event details. |

## Assets And Indicators

| Field | Description |
|---|---|
| `hosts` | List of hosts seen in the parsed events. |
| `users` | List of users seen in the parsed events. |
| `source_ips` | List of source IP addresses. |
| `destination_ips` | List of destination IP addresses. |
| `event_types` | List of event types found in the report. |

## Recommended Actions

Each recommended action should include:

| Field | Description |
|---|---|
| `priority` | Action priority, such as High, Medium, or Low. |
| `action` | Recommended response action. |
| `reason` | Why this action is recommended. |

## Raw Event Details

Each raw event detail should include:

| Field | Description |
|---|---|
| `event_id` | Matching timeline event ID. |
| `raw_event` | Full original event text or raw log line. |
| `parsed_fields` | Fields extracted from the raw event. |

## Known Limitations

Each limitation should include:

| Field | Description |
|---|---|
| `limitation` | Known limitation of the current pipeline. |
| `impact` | How the limitation affects the report. |

## Frontend Notes

The HTML report generator should display:

- Summary section
- Risk level section
- Key findings section
- Threat timeline section
- Assets and indicators section
- Recommended actions section
- Raw event details section
- Known limitations section

## Status

Completed for Week 6 frontend/backend handoff.