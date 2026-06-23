# Team Midterm Report

## https://github.com/Dredman72/security-log-threat-timeline

**Project:** Intelligent Security Log Summarization and Threat Timeline Generation  
**Course:** CSC 482 Capstone Project 2  
**Team:** Project Team 2  
**Team Members:** Derrick Redman, Zion Moore, Oriah Molton-Bowman  
**Reporting Period:** Weeks 1-4, June 1-June 28, 2026

## Project Overview

Our team project is a Flask-based security log analysis tool. The prototype allows a user to paste or upload security logs, sends the log content to the OpenAI API using the tested assignment model, and returns a structured security report. The report is designed to include an executive summary, risk level, attack type, affected assets, indicators of compromise, key findings, a chronological threat timeline with evidence, and recommended actions.

The goal is to help a security analyst or instructor understand raw security logs faster by reducing log noise, organizing events, and presenting the most important findings in a report-style format.

## Milestones Achieved

| Done | Dates | Milestone | Brief Description |
| --- | --- | --- | --- |
| [x] | June 1-7 | Week 1: Project kickoff and requirements | The team confirmed the project topic, team roles, initial scope, target log types, and the need for a runnable prototype. |
| [x] | June 8-14 | Week 2: Data model, sample logs, and output format | The team defined the shared backend, LLM, and frontend structure. Derrick created the LLM output format, Zion created the backend event schema and sample logs, and Oriah created the frontend report/timeline wireframe. |
| [x] | June 15-21 | Week 3: Log ingestion and parser validation | Zion completed an initial parser prototype and normalized output. Derrick created the parser output validation checklist. The team reviewed the parser structure against the fields needed for the LLM and report display. |
| [x] | June 22-28 | Week 4: LLM integration and structured summarization | Derrick refined the OpenAI prompt and fallback behavior so the model returns structured report sections and the app does not fail silently when output is incomplete or imperfect. |

## Subtasks Completed

### Week 1 Subtasks

| Member | Subtask | Brief Description |
| --- | --- | --- |
| Derrick | Initial prototype framework | Created the first Flask/OpenAI project structure with setup instructions and milestone TODO planning. |
| Derrick | Team coordination | Confirmed the project goal and helped organize team responsibilities. |
| Zion | Backend planning | Identified backend/log processing needs and the type of parser output required for the project. |
| Oriah | Frontend planning | Identified the frontend report sections and timeline display needs. |

### Week 2 Subtasks

| Member | Subtask | Brief Description |
| --- | --- | --- |
| Derrick | LLM prompt and JSON output draft | Defined the report fields the OpenAI output should include: executive summary, risk level, attack type, affected assets, IOCs, key findings, timeline events, evidence, and recommended actions. |
| Zion | Canonical event schema | Defined parsed event fields such as timestamp, source, host, user, event type, severity, description, evidence, and raw event. |
| Zion | Sample parser data | Created a sample CSV security log to support parser testing. |
| Oriah | Report/timeline wireframe | Created a PowerPoint wireframe showing how the final report and timeline should be organized. |

### Week 3 Subtasks

| Member | Subtask | Brief Description |
| --- | --- | --- |
| Derrick | Parser output validation checklist | Created `PARSER_OUTPUT_VALIDATION_CHECKLIST.md` to verify that backend parser output supports the LLM prompt and frontend report. |
| Derrick | Parser review | Reviewed Zion's parser output and recommended improvements such as source IP, destination IP, standardized event types, and raw event preservation. |
| Zion | Backend health check | Verified the parser prototype health check returned `status: ok`. |
| Zion | CSV parser test | Tested the parser using sample CSV logs and confirmed it parsed 4 events and identified 3 High/Critical events. |
| Zion | Normalized JSON output | Generated parser output using the canonical event schema. |
| Zion | Starter report output | Generated a starter HTML security report with an executive summary, validation warnings, and a threat timeline table. |
| Oriah | Frontend follow-up planning | Confirmed the need for sample parsed event data and the framework direction before building the Week 3/Week 4 placeholder. |

### Week 4 Subtasks

| Member | Subtask | Brief Description |
| --- | --- | --- |
| Derrick | Refined OpenAI summarization prompt | Improved prompt instructions so the model returns concise, structured JSON report output. |
| Derrick | Improved fallback handling | Added safer JSON parsing, report normalization, missing field defaults, and clear error messages for incomplete or invalid model output. |
| Derrick | Upload handling review | Clarified supported uploaded file types and added clear handling for raw `.evtx` files and oversized uploads. |
| Zion | Parser-to-LLM coordination | Continued preparing parser output so normalized events can be connected to the LLM workflow. |
| Oriah | Report section planning | Continued aligning frontend report sections with the structured LLM output fields. |

## Testing and Demo Evidence

The following tests were completed or prepared as evidence for the midterm report. Screenshots should be inserted into the submitted version of this report.

### Test 1: Flask Homepage Loads

**Purpose:** Confirm the web application starts correctly and displays the log input form.  
**Procedure:** The team ran the Flask application locally and opened `http://127.0.0.1:5000/`.  
**Expected Result:** The page displays the application title, paste-log text box, file upload control, and Analyze Logs button.  
**Result:** Passed. The Flask homepage loaded successfully.

**Screenshot Evidence:** Insert screenshot of Flask homepage.

### Test 2: OpenAI API Key and Usage

**Purpose:** Confirm the app can connect to OpenAI using the local `.env` API key without exposing the key.  
**Procedure:** Derrick confirmed the API key exists locally, ran the application, submitted sample logs, and checked the OpenAI usage page.  
**Expected Result:** OpenAI usage increases after analysis, and the application returns a report.  
**Result:** Passed. OpenAI usage showed API activity, confirming the app sent requests successfully.

**Screenshot Evidence:** Insert screenshot of OpenAI usage page with no API key shown.

### Test 3: Sample SSH and Firewall Log Analysis

**Purpose:** Confirm the app can summarize suspicious security activity and generate report sections.  
**Procedure:** Derrick pasted sample Linux SSH and firewall logs showing repeated failed SSH logins, a successful root login, a privileged command reading `/etc/shadow`, and a firewall block.  
**Expected Result:** The app returns an executive summary, risk level, attack type, affected assets, indicators of compromise, key findings, timeline events with evidence, and recommended actions.  
**Result:** Passed. The output was structured and demo-ready.

**Screenshot Evidence:** Insert screenshot showing sample logs pasted into the app and report output.

### Test 4: Threat Timeline Evidence

**Purpose:** Confirm timeline events include timestamp, source, severity, details, and supporting evidence.  
**Procedure:** The team reviewed the generated timeline section after submitting sample logs.  
**Expected Result:** Timeline events are chronological and include evidence from the original log lines.  
**Result:** Passed. Timeline entries included timestamps, source fields, severity badges, details, and evidence.

**Screenshot Evidence:** Insert screenshot of threat timeline section.

### Test 5: Parser Output Validation

**Purpose:** Confirm Zion's parser output matches the fields needed by the LLM and frontend.  
**Procedure:** Derrick reviewed Zion's normalized parser output against `PARSER_OUTPUT_VALIDATION_CHECKLIST.md`.  
**Expected Result:** Parser output includes required fields such as timestamp, source, host, user, event type, severity, description, evidence, and raw event.  
**Result:** Passed with improvement notes. Derrick recommended adding `source_ip` and `destination_ip` when available, standardizing event type names, and preserving the original raw event.

**Screenshot Evidence:** Insert screenshot of parser output and checklist review.

### Test 6: Fallback Behavior Review

**Purpose:** Confirm the app handles incomplete or imperfect OpenAI output gracefully.  
**Procedure:** Derrick updated the app so model output is normalized before display and missing fields are filled with safe defaults.  
**Expected Result:** The app does not crash when the model output is missing fields, incomplete, or wrapped in formatting.  
**Result:** Passed by code review and local function checks.

**Screenshot Evidence:** Insert screenshot of successful report output or terminal check if used.

## Lessons Learned

- The team learned that the backend parser, LLM prompt, and frontend report must share the same data structure.
- Derrick learned that structured prompt design is important because the frontend depends on consistent report fields.
- Zion's parser work showed that normalized event fields are necessary before the system can reliably summarize logs.
- Oriah's wireframe showed that frontend planning helps define what backend and LLM fields are needed.
- The team learned that GitHub collaboration requires clean file organization, clear commit messages, and avoiding private files such as `.env`.
- The team also learned that local testing and VM deployment are different. `127.0.0.1` works only on the computer running the app, while VM deployment requires the app to listen on the VM network and use port 80 or 443.

## Team Member Contributions

| Team Member | Role | Contributions So Far |
| --- | --- | --- |
| Derrick Redman | Team Leader + AI/LLM Specialist | Created the Flask/OpenAI prototype, confirmed the tested OpenAI model, refined the LLM prompt, improved fallback handling, created the parser validation checklist, updated README/project documentation, created GitHub repository, coordinated team direction, and reviewed team deliverables. |
| Zion Moore | Backend & Log Processing Lead | Created the canonical event schema, created sample CSV security logs, built the first parser prototype, ran backend health checks, parsed sample events, identified High/Critical events, generated normalized JSON output, and produced a starter HTML security report. |
| Oriah Molton-Bowman | Frontend & Visualization Lead | Created the Week 2 PowerPoint report/timeline wireframe, planned frontend sections, identified frontend data fields, planned timeline display behavior, and requested parsed sample data to continue the frontend placeholder. |

## Progress Compared to Plan

The team has progressed mostly according to the project plan, timeline, and schedule.

Weeks 1, 2, and 3 are complete. Derrick's Week 4 LLM prompt and fallback handling tasks are complete. Zion and Oriah still need to finish the Week 4 connection between parser output and the report display. This is consistent with the project plan because Week 4 focuses on connecting normalized events to the LLM workflow and preparing report sections.

## Plan Adjustment

No major plan adjustment is required. The team will continue using Flask and HTML as the shared framework. The next adjustment is a coordination step: Zion should provide sample normalized parser output to Oriah, and Derrick should help confirm that the parser output can be passed into the OpenAI workflow cleanly.

The Week 5 focus remains threat timeline generation logic and interactive timeline prototype work.

## Team Sign-Off

Each team member must sign before submission.

| Team Member | Role | Signature | Date |
| --- | --- | --- | --- |
| Derrick Redman | Team Leader + AI/LLM Specialist | ______________________________ | ______________ |
| Zion Moore | Backend & Log Processing Lead | ______________________________ | ______________ |
| Oriah Molton-Bowman | Frontend & Visualization Lead | ______________________________ | ______________ |
