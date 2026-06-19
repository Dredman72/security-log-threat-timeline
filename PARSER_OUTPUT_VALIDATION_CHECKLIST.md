# Parser Output Validation Checklist

## Purpose

This checklist defines what each parsed security log event should include before the event is sent to OpenAI for summarization and threat timeline generation.

Owner: Derrick Redman  
Week: 3  
Project Area: Parser output validation and LLM readiness

## Required Parsed Event Fields

Each parsed log event should include these fields whenever the information is available:

| Field | Required | Description | Example |
| --- | --- | --- | --- |
| `timestamp` | Yes | Date and time of the event. Use `Unknown` if missing. | `Jun 17 10:14:22` |
| `host` | Yes | System or device where the event occurred. | `webserver` |
| `source` | Yes | Log source, service, process, or tool. | `sshd`, `ufw`, `Windows Security` |
| `user` | If available | Username or account involved. | `admin`, `root`, `oracle` |
| `source_ip` | If available | External or internal source IP address. | `203.0.113.45` |
| `destination_ip` | If available | Destination IP address or system target. | `10.0.0.12` |
| `event_type` | Yes | Normalized event category. | `authentication_failure` |
| `severity` | Yes | Estimated severity. | `Low`, `Medium`, `High`, `Critical` |
| `description` | Yes | Plain-English explanation of the event. | `Failed SSH login for invalid user admin` |
| `raw_event` | Yes | Original unmodified log line. | Full original log line |
| `evidence` | Yes | Specific log detail supporting the event. | `Failed password for invalid user admin from 203.0.113.45` |

## Recommended Event Types

Use consistent event type labels so the backend, OpenAI prompt, and frontend timeline can work from the same vocabulary.

- `authentication_failure`
- `authentication_success`
- `privilege_escalation`
- `sensitive_file_access`
- `firewall_block`
- `malware_indicator`
- `suspicious_process`
- `lateral_movement`
- `account_change`
- `configuration_change`
- `unknown`

## Severity Guidelines

Use these rules as a starting point. Severity can be adjusted if surrounding events make the activity more serious.

| Severity | Meaning | Examples |
| --- | --- | --- |
| `Low` | Informational or blocked activity with limited impact. | Firewall block with no successful access |
| `Medium` | Suspicious activity that may indicate probing or early attack behavior. | Repeated failed logins, suspicious scan traffic |
| `High` | Strong evidence of compromise or unauthorized access attempt. | Successful login after repeated failures |
| `Critical` | Confirmed or highly likely compromise with sensitive access. | Root login followed by `/etc/shadow` access |

## Example Parsed Event

Raw log:

```text
Jun 17 10:14:22 webserver sshd[2214]: Failed password for invalid user admin from 203.0.113.45 port 51422 ssh2
```

Expected parsed output:

```json
{
  "timestamp": "Jun 17 10:14:22",
  "host": "webserver",
  "source": "sshd",
  "user": "admin",
  "source_ip": "203.0.113.45",
  "destination_ip": null,
  "event_type": "authentication_failure",
  "severity": "Medium",
  "description": "Failed SSH login for invalid user admin",
  "raw_event": "Jun 17 10:14:22 webserver sshd[2214]: Failed password for invalid user admin from 203.0.113.45 port 51422 ssh2",
  "evidence": "Failed password for invalid user admin from 203.0.113.45"
}
```

## Validation Checklist

Use this checklist when reviewing parser output.

- [ ] Each log line creates one parsed event or is intentionally skipped with a reason.
- [ ] Every parsed event includes a timestamp or `Unknown`.
- [ ] Every parsed event includes the original `raw_event`.
- [ ] Host, source, user, and IP fields are extracted when present.
- [ ] Event type uses one of the recommended normalized labels.
- [ ] Severity is assigned consistently.
- [ ] Description is clear enough for a security analyst to understand quickly.
- [ ] Evidence points to a specific log detail, not a vague summary.
- [ ] Parser does not invent fields not supported by the raw log.
- [ ] Parser output can be converted to JSON without errors.
- [ ] Parsed events can be sorted chronologically when timestamps are available.
- [ ] Output supports the OpenAI prompt fields: summary, risk level, affected assets, indicators of compromise, key findings, timeline, evidence, and recommended actions.

## Test Cases For Week 3

The parser should be tested against at least these scenarios:

1. SSH failed login attempt
2. SSH successful login
3. Firewall block
4. Sensitive file access
5. Windows failed login event
6. Missing timestamp
7. Malformed or unsupported log line

## Team Notes

Zion can use this checklist while building parser logic. Derrick will review parser output against this checklist before the output is sent to OpenAI. Oriah can use the same fields to plan frontend timeline and report display requirements.
