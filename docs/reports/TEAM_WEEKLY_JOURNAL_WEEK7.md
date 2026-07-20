# Team Weekly Journal - Week 7

**Project:** Intelligent Security Log Summarization and Threat Timeline Generation  
**Course:** CSC 482 Capstone Project 2  
**Team:** Project Team 2  
**Team Members:** Derrick Redman, Zion Moore, Oriah Molton-Bowman  
**Week:** Week 7, July 13-July 19, 2026  
**GitHub Repository:** https://github.com/Dredman72/security-log-threat-timeline  
**Status:** Updated draft - Derrick's Week 7 AI/LLM prompt consistency work and Zion's Week 7 integrated backend build evidence are included. Oriah's Week 7 frontend/UI polish update is still pending in the local files.

## Milestones Achieved

### Milestone 1: Prompt and Summary Consistency Improved

Derrick reviewed and improved the OpenAI prompt behavior for more consistent report summaries across different sample security logs. The Week 7 focus was making sure the generated summaries are clear, accurate, and useful for incident review.

This supports the project goal because the application depends on consistent LLM output to produce a reliable executive summary, risk level, attack type, indicators of compromise, key findings, timeline events, evidence, and recommended actions.

### Milestone 2: Week 7 Test Scenarios Prepared

Derrick prepared multiple sample log scenarios for testing summary consistency and report quality. These test logs help confirm that the application can handle different types of security activity instead of only one sample SSH incident.

Sample scenarios include SSH brute-force activity, firewall block events, suspicious PowerShell activity, EDR malware alerts, and mixed authentication/firewall/EDR events.

### Milestone 3: Integrated Application Review Started

The Flask application was reviewed as an integrated upload-to-report workflow. The current prototype can accept pasted or uploaded logs, generate an OpenAI-assisted report, display a threat timeline, show parsed event preview data, and provide downloadable JSON and HTML report outputs.

This milestone confirms the project is moving from separate prototype parts toward a combined team application.

### Milestone 4: Zion Integrated Backend Build Completed

Zion completed Week 7 integrated backend build evidence. His update documents the upload-to-report workflow, including file upload, log parsing, event normalization, event sorting/grouping, report-ready JSON generation, and timeline/report output.

This supports the project goal because the backend must move uploaded logs into report-ready data that can support the LLM summary and frontend timeline.

### Milestone 5: Oriah Frontend/UI Polish Pending Locally

No separate Week 7 frontend/UI polish update from Oriah was found in the local files during this update. Her section should be completed after her Week 7 frontend evidence is submitted or synced.

## Subtasks Completed

| Status | Member | Subtask | Brief Description |
| --- | --- | --- | --- |
| Completed | Derrick | Improved OpenAI prompt consistency | Reviewed and improved prompt behavior so summaries are more stable across different sample log types. |
| Completed | Derrick | Prepared Week 7 test scenarios | Added/reviewed sample logs for SSH brute force, firewall-only activity, suspicious PowerShell, EDR malware alert, and mixed events. |
| Completed | Derrick | Reviewed Flask report output | Confirmed the application still produces the expected report sections after analyzing sample security logs. |
| Completed | Derrick | Reviewed downloadable report output | Confirmed JSON and HTML report downloads support testing evidence and report review. |
| Completed | Zion | Completed integrated backend build review | Documented upload-to-report backend workflow, test scenarios, correlation fields, error handling checks, and report-ready JSON evidence. |
| Pending | Oriah | Polish timeline and report UI | Pending teammate update. Expected focus: cleaner visual layout, labels, and report sections. |

## Testing of Subtasks With Evidence

### Test 1: Week 7 Prompt Consistency Documentation Review

**Purpose:** Confirm Derrick's Week 7 LLM work is documented and tied to the project milestone.  
**Procedure:** Derrick reviewed the Week 7 prompt consistency notes and checked that they describe how summaries should stay accurate, clear, and useful across sample scenarios.  
**Expected Result:** Documentation should explain the purpose of the Week 7 prompt consistency work and identify the sample logs used for review.  
**Result:** Passed. The Week 7 prompt consistency documentation supports Derrick's Week 7 milestone.

**Screenshot Evidence:** Insert screenshot of `docs/week7-prompt-summary-consistency.md`.


### Test 2: Week 7 Sample Log Set Review

**Purpose:** Confirm the project includes multiple sample logs for testing summary consistency.  
**Procedure:** Derrick reviewed the test log folder and confirmed that multiple sample security scenarios are available.  
**Expected Result:** The test folder should include several different log types, not only one SSH example.  
**Result:** Passed. The project includes sample logs for SSH brute-force/root access, firewall block only, suspicious PowerShell, EDR malware alert, and mixed authentication/firewall/EDR activity.

**Screenshot Evidence:** Insert screenshot of `examples/test_logs/`.

### Test 3: Flask Summary Consistency Review

**Purpose:** Confirm the Flask app still generates a clear report summary, risk level, attack type, and risk rationale after the Week 7 prompt consistency improvements.  
**Procedure:** Derrick ran the Flask prototype locally, pasted or uploaded a sample log, and clicked **Analyze Logs**.  
**Expected Result:** The report should produce a clear executive summary, correct risk level, attack type, and risk rationale without confusing or inconsistent wording.  
**Result:** Passed for Derrick's current sample test. The report summary was understandable and tied the risk level to evidence in the logs.

**Screenshot Evidence:** Insert screenshot of the Flask report summary, risk level, attack type, and risk rationale.

### Test 4: Downloaded JSON and HTML Report Review

**Purpose:** Confirm the generated report can still be saved for testing evidence and submission support.  
**Procedure:** Derrick used the **Download JSON** and **Download HTML** buttons after generating a report.  
**Expected Result:** The downloaded report files should preserve the generated summary, timeline, evidence, findings, and recommended actions.  
**Result:** Passed. The app provides downloadable outputs that can be used as testing evidence or included in project documentation.

**Screenshot Evidence:** Insert screenshot of the downloaded JSON output and/or downloaded HTML report.

### Test 5: Zion Integrated Backend Build Review

**Purpose:** Confirm Zion's Week 7 backend work supports the integrated upload-to-report workflow.  
**Procedure:** Derrick reviewed Zion's Week 7 integrated application build documentation and example JSON evidence.  
**Expected Result:** Zion's backend work should describe file upload, parsing, event normalization, sorting/grouping, report-ready data generation, and timeline/report output.  
**Result:** Passed. Zion's Week 7 backend evidence documents the integrated workflow, test scenarios, correlation fields, error checks, and report-ready JSON output.

**Screenshot Evidence:** 


### Test 6: Oriah Frontend/UI Polish Review Pending

**Purpose:** Confirm Oriah's Week 7 frontend work improves report readability and timeline scanning.  
**Procedure:** The team will review Oriah's Week 7 frontend/report UI polish once her update is available locally.  
**Expected Result:** The report should be easier to scan, with clear labels, organized sections, and readable timeline/report layout.  
**Result:** Pending. No separate Oriah Week 7 frontend/UI polish evidence was found in the local files during this update.

**Screenshot Evidence:** Insert screenshot of Oriah's Week 7 report/timeline UI polish after it is submitted or synced.

## Lessons Learned

This week reinforced that LLM output quality depends on both prompt structure and test coverage. A prompt may work well for one sample log but still need testing against multiple scenarios to confirm consistent behavior.

The team also learned that integration work requires clear handoffs. Derrick's LLM output, Zion's parser output, and Oriah's frontend display must use compatible fields so the final report works as one complete application.

## Contribution of Each Team Member

### Derrick Redman - Team Lead and AI/LLM Specialist

Derrick prepared the Week 7 prompt and summary consistency work. He reviewed the Flask/OpenAI report output, confirmed the application can still generate structured security reports, tested multiple sample log scenarios, and reviewed downloaded JSON/HTML report output as evidence. Derrick also updated this Week 7 journal so the team can track completed and pending Week 7 work.

### Zion Moore - Backend and Log Processing Lead

Zion completed Week 7 integrated backend build evidence. His work documents the upload-to-report backend workflow, parser integration steps, normalized event handling, sorting/grouping behavior, report-ready JSON output, correlation fields, and error-handling checks. His update helps confirm the backend can support the shared Flask/HTML report workflow.

### Oriah Molton-Bowman - Frontend and Visualization Lead

Oriah's Week 7 contribution is still pending in the local files at the time of this update. Her planned Week 7 responsibility is to polish the timeline and report UI so the final report is easier to scan and understand. This section should be updated after Oriah submits or syncs her Week 7 frontend evidence.

## Team Meeting Attendance

| Date | Participants | Duration | Purpose / Notes |
| --- | --- | --- | --- |
| To be added | Derrick / Zion / Oriah | To be added | Add Week 7 team meeting details before final submission. |

## Progress Compared to Project Plan

The team is progressing according to the Week 7 project plan. Derrick's AI/LLM prompt consistency work is complete, and Zion's integrated backend build evidence is complete.

Week 7 is not fully finalized until Oriah's frontend/report UI polish evidence is submitted or synced into the local project files.

## Plan Adjustment

No major plan adjustment is needed right now. The team should continue using the shared Flask/HTML prototype as the main integration target.

If Oriah's frontend update is delayed, the journal should remain an updated draft until her Week 7 evidence is added. Derrick and Zion's completed Week 7 work can remain documented as current progress.

## Next Steps

| Member | Next Step |
| --- | --- |
| Derrick | Add final screenshots and keep Week 7 prompt consistency evidence organized. |
| Zion | Confirm whether any additional Week 7 backend screenshots should be added to the journal. |
| Oriah | Submit or sync Week 7 frontend/timeline/report UI polish evidence. |
| Team | Review the combined Week 7 work and confirm the prototype remains demo-ready. |

## Team Sign-Off

By signing below, each team member confirms that they reviewed the Week 7 journal and that their contribution summary is accurate.

| Name | Signature | Date |
| --- | --- | --- |
| Derrick Redman |  |  |
| Zion Moore |  |  |
| Oriah Molton-Bowman |  |  |
