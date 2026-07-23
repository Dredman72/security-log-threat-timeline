# Week 8: Zion Backend Walkthrough

## Owner

Zion Moore

## Focus

Final backend demo preparation, parser explanation, and sample output review.

## Goal

Prepare a clear backend walkthrough for the final capstone presentation so the team can explain how raw security logs become normalized events and report-ready timeline data.

## Backend Walkthrough

The final backend walkthrough should explain this workflow:

1. A user uploads or pastes sample security log data.
2. The backend parser reads the submitted log content.
3. Parsed events are normalized into the shared event schema.
4. Events are sorted chronologically for timeline generation.
5. Events are grouped by investigation fields such as host, user, IP address, event type, and severity.
6. Report-ready data is passed into the OpenAI summarization workflow and frontend report view.

## Parser Output Fields

Zion's backend output supports the fields needed by the LLM prompt and frontend report:

| Field | Purpose |
| --- | --- |
| `timestamp` | Places the event in chronological order |
| `source` | Identifies the log source, such as Windows, Sysmon, firewall, or EDR |
| `host` | Shows the affected system |
| `user` | Shows the related account when available |
| `source_ip` | Supports network and login investigation |
| `destination_ip` | Supports network and firewall correlation |
| `event_type` | Categorizes the activity |
| `severity` | Helps prioritize investigation |
| `description` | Provides a human-readable event explanation |
| `evidence` | Preserves the detail used to support the finding |
| `raw_event` | Keeps the original event text or row for traceability |

## Demo Dataset Notes

The final demo can use the sample logs in `examples/test_logs/`:

- `windows_powershell_suspicious.log`
- `ssh_bruteforce_root_access.log`
- `mixed_auth_firewall_edr.log`
- `firewall_block_only.log`
- `edr_malware_alert.log`

These samples cover suspicious PowerShell activity, brute force login behavior, firewall events, EDR malware alerts, mixed severities, and multi-source log correlation.

## Evidence Files

Zion's Week 8 backend walkthrough builds on the completed Week 7 backend evidence:

- `docs/week7-integrated-application-build.md`
- `examples/week7-integrated-build-test.json`
- `examples/test_logs/`

## Presentation Talking Points

- The parser converts raw log text into consistent structured events.
- Normalized fields make it easier for the LLM to summarize activity without losing key evidence.
- Chronological sorting supports the attack timeline.
- Grouping and correlation fields help identify related activity across users, hosts, IP addresses, and log sources.
- Preserving raw event evidence helps an analyst verify why a timeline event or finding was generated.

## Status

Completed for Zion's Week 8 backend walkthrough and final demo preparation.
