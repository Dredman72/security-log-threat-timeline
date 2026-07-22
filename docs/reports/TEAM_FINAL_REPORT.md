# Team Final Report

## GitHub Repository: https://github.com/Dredman72/security-log-threat-timeline

**Project:** Intelligent Security Log Summarization and Threat Timeline Generation  
**Course:** CSC 482 Capstone Project 2  
**Team:** Project Team 2  
**Team Members:** Derrick Redman, Zion Moore, Oriah Molton-Bowman  
**Planning Window:** June 1-July 28, 2026  
**Final Presentation Window:** July 27-28, 2026

## Project Goal

The goal of this project is to build a Flask web application that accepts pasted or uploaded security logs, sends the log content to the OpenAI API, and generates a structured security report. The report includes an executive summary, risk level, attack type, risk rationale, affected assets, indicators of compromise, key findings, a chronological threat timeline with evidence, parsed event preview, recommended actions, and downloadable JSON/HTML report output.

## Milestones Achieved

| Done | Week | Milestone | Brief Description |
| --- | --- | --- | --- |
| [x] | Week 1 | Project kickoff and requirements | Team project topic, scope, roles, lab setup, and OpenAI API plan were established. |
| [x] | Week 2 | Initial prototype framework and planning | Individual prototype work began. Derrick created the Flask/OpenAI prototype direction and LLM JSON output structure. Zion created the backend event schema and sample parser data. Oriah created the report/timeline wireframe. |
| [x] | Week 3 | Parser validation and early integration planning | Derrick created the parser output validation checklist. Zion tested parser normalization. Oriah planned the parsed-event display requirements. |
| [x] | Week 4 | LLM integration and structured summarization | Derrick improved the OpenAI prompt and fallback behavior. Zion created AI-ready parser input documentation. Oriah documented report section labels and frontend display expectations. |
| [x] | Week 5 | Threat timeline generation | Derrick refined timeline event wording, evidence rules, and prompt requirements. Zion documented sorting/grouping logic. Oriah continued timeline/report visualization planning. |
| [x] | Week 6 | End-to-end report generation | The app supported pasted/uploaded logs, report timestamp, risk rationale, reset workflow, downloadable JSON/HTML reports, parsed event preview, and improved report sections. |
| [x] | Week 7 | Integration testing and quality improvement | Derrick added reusable sample logs and prompt consistency checks. Zion added integrated backend build evidence. Oriah polished the frontend report UI and added screenshot evidence. |
| [ ] | Week 8 | Final hardening, documentation, and presentation preparation | Final report drafting has started. Oriah completed frontend walkthrough notes for the final demo. Remaining work is final evidence review, presentation/demo polish, and team signatures. |

## Subtasks Completed

### Derrick Redman - Team Lead and AI/LLM Specialist

Derrick created and refined the Flask/OpenAI prototype. His work included the OpenAI prompt, structured JSON report format, fallback behavior for incomplete model output, threat timeline rules, risk rationale, report timestamp, reset workflow, downloadable JSON/HTML report output, parsed event preview improvements, and Week 7 sample log testing.

### Zion Moore - Backend and Log Processing Lead

Zion created the canonical backend event schema, sample parser logs, parser prototype output, normalized JSON examples, AI-ready parser input, backend upload-to-report pipeline documentation, and Week 7 integrated backend build evidence. His work supports the parser-to-LLM handoff and ensures parsed logs contain fields needed for reporting.

### Oriah Molton-Bowman - Frontend and Visualization Lead

Oriah created the report and timeline wireframe, planned the frontend report sections, identified required data fields for display, polished `templates/index.html`, added screenshot evidence, and prepared Week 8 frontend walkthrough notes. Her work supports the user-facing report structure, timeline display, and final presentation visuals.

## Testing of Subtasks With Evidence

### Test 1: Flask Homepage Loads

**Purpose:** Confirm the Flask prototype starts locally and displays the Analyze Logs page.  
**Procedure:** Derrick ran the local Flask app and opened `http://127.0.0.1:5000/`.  
**Expected Result:** The page should show the security log input area, upload field, and Analyze Logs button.  
**Result:** Passed.

![Flask app homepage](../screenshots/Flask%20App%20Homepage.png)

### Test 2: OpenAI API Usage Confirmation

**Purpose:** Confirm the project connects to OpenAI through Derrick's API key and generates usage.  
**Procedure:** Derrick ran the app, submitted sample logs, and reviewed the OpenAI usage dashboard.  
**Expected Result:** OpenAI usage should increase after the app analyzes logs.  
**Result:** Passed.

![OpenAI usage dashboard](../screenshots/OpenAI%20Usage%20Dashboard.png)

### Test 3: Structured OpenAI Report Output

**Purpose:** Confirm the model returns structured report data that supports the required project sections.  
**Procedure:** Derrick pasted sample SSH/security logs into the Flask app and clicked Analyze Logs.  
**Expected Result:** The app should display a report summary, risk level, attack type, key findings, timeline, evidence, and recommended actions.  
**Result:** Passed.

![OpenAI report output](../screenshots/OpenAI%20Report%20Output.png)

### Test 4: Parser Output Validation

**Purpose:** Confirm Zion's parser output supports the LLM and frontend fields.  
**Procedure:** Derrick reviewed Zion's normalized parser output against the parser output validation checklist.  
**Expected Result:** Parser output should include timestamp, source, host, user, event type, severity, description, evidence, and raw event.  
**Result:** Passed with improvement notes for source IP, destination IP, and standardized event type names.

![Parser output checklist](../screenshots/Parser%20Output%20Validation%20Checklist.png)

![Updated normalized JSON](../screenshots/Updated%20Normalized%20Events%20JSON.png)

### Test 5: Threat Timeline Rules and Grouping

**Purpose:** Confirm the prompt supports concise chronological timeline generation with evidence.  
**Procedure:** Derrick updated and reviewed the timeline rules in the OpenAI prompt, then tested grouped timeline output.  
**Expected Result:** Timeline events should include timestamp, source, event, severity, details, and evidence. Repeated similar events should be grouped when appropriate.  
**Result:** Passed.

![OpenAI prompt timeline rules](../screenshots/OpenAI%20Prompt%20Timeline%20Rules.png)

![Grouped timeline JSON](../screenshots/Grouped%20Timeline%20JSON.png)

### Test 6: End-to-End Report Generation

**Purpose:** Confirm the Week 6 workflow creates a complete report from pasted or uploaded logs.  
**Procedure:** Derrick generated a report after the Week 6 improvements and reviewed the report sections.  
**Expected Result:** The app should show summary, risk level, risk rationale, assets, IOCs, key findings, timeline, parsed event preview, recommended actions, and download options.  
**Result:** Passed.

![Week 6 HTML report generator](../screenshots/Week%206%20HTML%20Report%20Generator.png)

### Test 7: Frontend Wireframe and Report Planning

**Purpose:** Confirm the frontend planning supports the report/timeline sections needed by the project.  
**Procedure:** Oriah created report and timeline wireframe slides and listed the fields needed for display.  
**Expected Result:** The wireframe should support summary, risk, key findings, timeline, indicators/evidence, recommendations, and raw event details.  
**Result:** Passed for planning and design direction.

![Frontend wireframe](../screenshots/Wirefram%20Powerpoint.png)

![Frontend wireframe details](../screenshots/Wirefram%20Powerpoint2.png)

### Test 8: GitHub Collaboration and Documentation

**Purpose:** Confirm the project repository contains the shared source code, README, milestone tracking, and supporting documentation.  
**Procedure:** Derrick reviewed the GitHub repository after team uploads and documentation updates.  
**Expected Result:** The repository should contain app source code, templates, README, milestone TODOs, parser validation, demo/deployment guides, examples, and documentation.  
**Result:** Passed.

### Test 9: Week 8 Frontend Walkthrough Preparation

**Purpose:** Confirm Oriah's Week 8 frontend walkthrough is ready for the final presentation.  
**Procedure:** Oriah prepared `docs/week8-oriah-frontend-walkthrough.md` using the polished report UI screenshot and the updated `templates/index.html` interface.  
**Expected Result:** The walkthrough should explain the upload form, report summary, risk panel, key findings, assets/indicators, timeline search/filter controls, raw event preview, recommended actions, downloads, and known limitations.  
**Result:** Passed.

![Week 7 polished report UI](../screenshots/week7-ui.png)

![GitHub repository screenshot](../screenshots/GitHub%20Repository%20Screenshot.png)

## Lessons Learned

- The team learned that the LLM prompt must be specific about output fields, evidence, risk rationale, and timeline formatting to produce useful security reports.
- The team learned that backend parser fields must align with frontend report fields before integration can work smoothly.
- The team learned that repeated events, such as failed logins, should often be grouped so the timeline stays readable.
- The team learned that GitHub collaboration requires careful branching, commits, conflict resolution, and documentation updates.
- The team learned that final report evidence should be captured continuously instead of waiting until the end.

## Contribution of Each Team Member

| Team Member | Role | Contributions |
| --- | --- | --- |
| Derrick Redman | Team Lead and AI/LLM Specialist | Led project coordination, created and refined the Flask/OpenAI prototype, designed the structured JSON output, improved timeline prompt rules, added risk rationale, added reset/download features, tested sample logs, maintained README/milestone documentation, and drafted final report documentation. |
| Zion Moore | Backend and Log Processing Lead | Created the backend event schema, parser prototype, sample logs, normalized JSON output, AI-ready parser input, upload-to-report pipeline documentation, and Week 7 integrated backend build evidence. |
| Oriah Molton-Bowman | Frontend and Visualization Lead | Created the report/timeline wireframe, planned frontend report sections, identified required display fields, polished the final HTML report UI, added screenshot evidence, and prepared Week 8 frontend walkthrough notes for the final demo. |

## Team Meeting Attendance

| Date | Attendees | Topic | Duration |
| --- | --- | --- | --- |
| June 3, 2026 | Derrick, Zion, Oriah | Project kickoff and role discussion | 1h 1m |
| June 8, 2026 | Derrick, Zion, Oriah | Initial project planning and assignment review | 54m |
| June 10, 2026 | Derrick, Zion, Oriah | Project plan, timeline, and schedule | 1h 22m |
| June 17, 2026 | Derrick, Zion | Parser and LLM structure discussion | 43m |
| June 18, 2026 | Derrick, Zion, Oriah | Team integration planning and weekly progress | 3h 15m |
| June 21, 2026 | Derrick, Zion | Backend parser/schema review | 1h 9m |
| June 22, 2026 | Derrick, Zion | Parser validation and milestone review | 1h 43m |
| June 24, 2026 | Derrick, Oriah | GitHub and frontend coordination | 26m |
| July 11, 2026 | Derrick, Oriah | Week 6 status and report layout review | 30m |
| July 12, 2026 | Derrick, Zion, Oriah | Week 6 completion, roles, and next steps | 1h |
| Week 7/8 | Team discussion | Roles, completed milestones, and next steps for final report/demo | Ongoing |

## Progress Compared to Plan

The team has progressed according to the project plan overall. The core project is functional locally and supports the main workflow: users can paste or upload logs, analyze them with OpenAI, review structured report sections, inspect a chronological timeline, view parsed event previews, and download JSON/HTML report evidence.

The main remaining Week 8 items are final documentation polish, final presentation preparation, final backend evidence collection from Zion, and signatures from every team member before submission.

## Plan Adjustment

No major scope change is needed. The plan for Week 8 is to focus on final hardening, final documentation, final screenshots, final demo flow, and team sign-off. If any final frontend or backend changes arrive late, the team will document them in the final report and keep the README/milestones updated.

## Team Sign-Off

Each team member must sign before submission. Team members without signatures may receive zero credit according to the assignment instructions.

| Member | Printed Name | Signature | Date |
| --- | --- | --- | --- |
| Derrick Redman | Derrick Redman |  |  |
| Zion Moore | Zion Moore |  |  |
| Oriah Molton-Bowman | Oriah Molton-Bowman |  |  |
