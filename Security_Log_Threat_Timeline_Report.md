# Security Log Threat Timeline Report

Converted from PowerPoint: Security_Log_Threat_Timeline_Report.pptx

## Slide 1: Security Log Threat Timeline Report

Generated from CSV Parser Test 1
Oriah Molton-Bowman

## Slide 2: Executive Summary

The uploaded log indicates a likely multi-stage attack against WIN-SERVER-01 involving suspicious PowerShell activity, blocked outbound traffic, failed logins, and a critical ransomware alert.

## Slide 3: Key Findings

- Encoded PowerShell command
- Blocked suspicious IP 203.0.113.10
- Multiple failed logins
- Critical ransomware behavior detected

## Slide 4: Recommendations

- Isolate WIN-SERVER-01
- Investigate PowerShell execution
- Review accounts
- Perform malware forensics
- Verify backups

## Slide 5: Threat Timeline

13:00 High - Process Start (alice)
PowerShell launched with encoded command
13:05 High - Firewall Block (unknown)
Blocked suspicious outbound IP
13:11 Medium - Login Failure (bob)
Three failed login attempts
13:20 Critical - Malware Alert (alice)
Possible ransomware behavior

## Slide 6: Raw Event Details

13:00 | High | process_start | WIN-SERVER-01 | alice | Encoded command
13:05 | High | firewall_block | WIN-SERVER-01 | unknown | IP 203.0.113.10
13:11 | Medium | login_failure | WIN-SERVER-01 | bob | Three failed attempts
13:20 | Critical | malware_alert | WIN-SERVER-01 | alice | Rapid file encryption

