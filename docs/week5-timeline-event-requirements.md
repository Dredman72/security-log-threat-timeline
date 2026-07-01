# Week 5 Timeline Event Wording and Evidence Requirements

**Project:** Intelligent Security Log Summarization and Threat Timeline Generation  
**Owner:** Derrick Redman  
**Week:** Week 5, June 29-July 5, 2026  
**Purpose:** Define how timeline events should be written and what evidence each event must include.

## Goal

The threat timeline should help a user understand what happened, when it happened, where it happened, and why the event matters. Each timeline event must be clear enough for a security analyst, instructor, or team member to trace the event back to the original log evidence.

## Required Timeline Fields

Each timeline event must include these fields:

| Field | Requirement |
| --- | --- |
| `timestamp` | Use the exact timestamp from the log when available. If missing, use `Unknown` and keep the event in the order it appeared. |
| `source` | Identify the log source, host, process, account, IP address, or service tied to the event. |
| `event` | Use a short event title written in analyst-friendly language. |
| `severity` | Use one of: `Low`, `Medium`, `High`, or `Critical`. |
| `details` | Explain what happened and why it matters in 1-2 clear sentences. |
| `evidence` | Include the specific log line, event ID, IP address, username, command, file path, or artifact that supports the event. |

## Timeline Wording Rules

Timeline event titles should be short, specific, and action-focused.

Good event title examples:

- `SSH failed login for invalid admin user`
- `Successful root SSH login from external IP`
- `Sensitive file accessed through sudo`
- `Firewall blocked inbound SSH traffic`
- `PowerShell launched suspicious encoded command`
- `EDR reported possible ransomware behavior`

Avoid vague titles:

- `Suspicious activity`
- `Security event`
- `Possible issue`
- `Something happened`

## Details Field Rules

The `details` field should explain the event without exaggerating beyond the logs.

Use:

- Clear security meaning.
- Plain English.
- One or two sentences.
- Evidence-supported wording.

Avoid:

- Guessing attacker intent without evidence.
- Calling something malware unless the log supports it.
- Adding facts not shown in the logs.
- Long paragraphs that make the timeline hard to scan.

## Evidence Requirements

Every timeline event must include evidence. Evidence should be specific enough that someone can compare the event to the original log.

Acceptable evidence examples:

- Original log line.
- Event ID.
- Source IP or destination IP.
- Username or host.
- Process name.
- Command line.
- File path.
- Firewall rule or blocked port.
- Alert name from EDR or antivirus.

Weak evidence examples:

- `The logs show this.`
- `Suspicious login activity.`
- `Possible attack detected.`

## Severity Guidance

| Severity | When to Use |
| --- | --- |
| `Low` | Informational or blocked activity with limited impact. |
| `Medium` | Suspicious attempts, repeated failures, reconnaissance, or activity needing review. |
| `High` | Confirmed suspicious behavior, successful access, privilege misuse, or strong indicator of compromise. |
| `Critical` | Successful compromise, credential theft, ransomware behavior, sensitive file access, or active malicious execution. |

## Example Timeline JSON Output

```json
[
  {
    "timestamp": "Jun 17 10:14:22",
    "source": "webserver sshd[2214]",
    "event": "SSH failed login for invalid admin user",
    "severity": "Medium",
    "details": "An external host attempted SSH authentication using the invalid username admin. This may indicate reconnaissance or brute-force behavior.",
    "evidence": "Jun 17 10:14:22 webserver sshd[2214]: Failed password for invalid user admin from 203.0.113.45 port 51422 ssh2"
  },
  {
    "timestamp": "Jun 17 10:15:02",
    "source": "webserver sshd[2288]",
    "event": "Successful root SSH login from external IP",
    "severity": "Critical",
    "details": "The root account successfully authenticated from an external IP address. This is a strong indicator of unauthorized access if the login was not expected.",
    "evidence": "Jun 17 10:15:02 webserver sshd[2288]: Accepted password for root from 203.0.113.45 port 51488 ssh2"
  },
  {
    "timestamp": "Jun 17 10:16:10",
    "source": "webserver sudo",
    "event": "Sensitive file accessed through sudo",
    "severity": "Critical",
    "details": "The root user executed a command to read /etc/shadow, which contains password hash data. This could support credential theft or offline password cracking.",
    "evidence": "Jun 17 10:16:10 webserver sudo: root : TTY=pts/0 ; PWD=/root ; USER=root ; COMMAND=/usr/bin/cat /etc/shadow"
  }
]
```

## Team Usage

- Derrick uses this document to keep OpenAI timeline output consistent.
- Zion uses this document to make sure parser output includes enough fields for timeline evidence.
- Oriah uses this document to design timeline cards, labels, severity badges, and expandable evidence sections.

## Completion Measurement

This Week 5 Derrick task is complete when timeline events consistently include:

- Timestamp.
- Source.
- Severity.
- Short event title.
- Clear details.
- Specific evidence.
