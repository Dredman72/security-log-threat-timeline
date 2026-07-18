# Week 7: Prompt and Summary Consistency Notes

## Purpose

This document records Derrick's Week 7 AI/LLM task: improving prompt consistency so OpenAI summaries remain clear, accurate, and consistent across different security log samples.

## Week 7 Goal

Improve prompts and summary consistency.

## Prompt Improvements Completed

- Added severity consistency rules so Low, Medium, High, and Critical have clear meanings across test logs.
- Added executive summary wording rules so summaries follow the same pattern:
  affected system or account, main event sequence, impact, and risk level.
- Added contradiction prevention rules so `executive_summary`, `risk_level`, and `risk_rationale` stay aligned.
- Added consistent attack type naming rules for common security scenarios:
  Brute Force, Credential Access, Privilege Escalation, Malware, Reconnaissance, Lateral Movement, Data Exfiltration, and Firewall/Network Block.
- Added alignment rules so key findings and recommended actions match the same incident narrative used in the executive summary.

## Expected Output Fields

The OpenAI output should continue to include:

- `executive_summary`
- `risk_level`
- `risk_rationale`
- `attack_type`
- `affected_assets`
- `indicators_of_compromise`
- `key_findings`
- `timeline`
- `recommended_actions`

## Test Notes

The following reusable sample logs were added under `examples/test_logs/` for Week 7 testing:

| Test Log | Scenario | Expected Risk | Expected Attack Type | Expected Summary Behavior | Status |
| --- | --- | --- | --- | --- | --- |
| `examples/test_logs/ssh_bruteforce_root_access.log` | SSH brute force followed by successful root login and `/etc/shadow` access | Critical | Brute Force / Credential Access / Privilege Escalation | Summary should mention repeated failed SSH attempts, successful root access, sensitive file access, and high-impact risk. | Ready to test |
| `examples/test_logs/firewall_block_only.log` | Firewall blocks inbound RDP and SSH attempts | Low or Medium | Firewall/Network Block or Reconnaissance | Summary should describe blocked probing without claiming compromise. | Ready to test |
| `examples/test_logs/windows_powershell_suspicious.log` | Suspicious PowerShell command, network connection, and script drop | High | Malware or Suspicious Process | Summary should mention suspicious PowerShell behavior, encoded command, network connection, and dropped script. | Ready to test |
| `examples/test_logs/edr_malware_alert.log` | EDR malware and rapid file encryption alerts | Critical | Malware | Summary should mention malware indicator, encryption behavior, affected host/user, and containment evidence. | Ready to test |
| `examples/test_logs/mixed_auth_firewall_edr.log` | VPN auth success after failures, lateral access, and suspicious file activity | Critical | Credential Access / Lateral Movement / Data Access | Summary should connect VPN login, internal SMB access, suspicious command activity, and payroll file access. | Ready to test |

### Test 1: SSH Brute Force and Root Login

Expected behavior:

- Summary identifies repeated SSH failures followed by successful root access.
- Risk level is High or Critical depending on sensitive follow-up activity.
- Attack type includes Credential Access and may include Brute Force or Privilege Escalation.
- Timeline groups repeated failed logins when possible.

### Test 2: Firewall Block Only

Expected behavior:

- Summary describes blocked network activity without claiming compromise.
- Risk level should usually be Low or Medium unless other evidence exists.
- Attack type should be Firewall/Network Block or Reconnaissance.
- Recommended actions should focus on monitoring, blocking, and log review.

### Test 3: Malware or Suspicious Process

Expected behavior:

- Summary identifies the suspicious process or malware indicator.
- Risk level should increase when execution, persistence, or data access is shown.
- Attack type should include Malware when supported by the logs.
- Evidence should cite process name, command line, file path, hash, or alert text.

## Measurement

This Week 7 task is complete when summaries are consistent across test logs and the report does not contradict itself between summary, risk level, risk rationale, attack type, timeline events, and recommended actions.

## Status

Completed for Derrick's Week 7 role.
