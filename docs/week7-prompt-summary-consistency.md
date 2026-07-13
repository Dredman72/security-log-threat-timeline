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
