# Capstone Project Plan

**Intelligent Security Log Summarization and Threat Timeline Generation**

| Field | Details |
| --- | --- |
| Project | Intelligent Security Log Summarization and Threat Timeline Generation |
| Course | CSC 482 Capstone Project 2 |
| Team | Project Team 2: Derrick Redman, Zion Moore, Oriah Molton-Bowman |
| Team Lead | Derrick Redman |
| Planning Window | June 1-July 28, 2026 |
| Final Presentation | July 27-28, 2026 |
| Primary Deliverable | Flask web application that accepts security logs, summarizes likely threats with OpenAI, and generates a chronological threat timeline report |
| Repository | Public GitHub repository for source code, project plan, milestone tracking, and team collaboration |

## Project Goal

Build a web-based security log analysis tool that allows a user to upload or paste security logs from sources such as Windows Event Logs, Linux authentication logs, firewall logs, Sysmon logs, and EDR-style alerts. The system will parse and normalize log activity, use the OpenAI API to summarize important security events, and generate a clear chronological threat timeline.

The final application should help a security analyst or instructor quickly understand what happened in a set of logs, what the risk level is, what evidence supports the finding, and what actions should be taken next.

## Core Capabilities

- Upload or paste raw security logs through a Flask web interface.
- Parse or normalize log events into a consistent event structure.
- Use the OpenAI API with the model tested in the OpenAI API key assignment, configured through `.env` and `app.py`.
- Generate an executive summary of likely security activity.
- Identify risk level, attack type, affected assets, and indicators of compromise.
- Generate key findings and recommended analyst actions.
- Create a chronological threat timeline with supporting evidence.
- Display the generated report in a browser.
- Support local execution on a student desktop, Windows Server 2025, and Ubuntu 24.04 LTS.

## Team Roles

| Member | Role | Responsibilities |
| --- | --- | --- |
| Derrick Redman | Team Leader + AI/LLM Specialist | Project coordination, OpenAI integration, prompt engineering, structured output design, report quality review, final presentation leadership |
| Zion Moore | Backend & Log Processing Lead | Log ingestion, parsing logic, normalized event schema, parser validation, backend workflow, sample log testing |
| Oriah Molton-Bowman | Frontend & Visualization Lead | Web interface, report layout, timeline visualization, user experience, frontend polish |

## Current Prototype Structure

```text
CapstoneProject/
  app.py
  requirements.txt
  README.md
  PROJECT_PLAN.md
  PARSER_OUTPUT_VALIDATION_CHECKLIST.md
  MILESTONE_TODOS.md
  DEMO_WORKFLOW_INSTRUCTIONS.md
  DEPLOYMENT_AND_SUBMISSION_GUIDE.md
  TEAM_MIDTERM_REPORT.md
  TEAM_WEEKLY_JOURNAL_WEEK4.md
  .env.example
  .gitignore
  templates/
    index.html
  uploads/
    .gitkeep
```

## Weekly Progress Summary

| Week | Status | Work Completed |
| --- | --- | --- |
| Week 1 | Complete | Project scope, initial Flask prototype, OpenAI API plan, setup instructions, and team role alignment |
| Week 2 | Complete | LLM prompt/output structure, backend event schema planning, sample parser data, and frontend report planning |
| Week 3 | Complete | Parser output validation checklist, first backend parser prototype review, normalized JSON review, starter report validation, and parsed-event frontend placeholder planning |
| Week 4 | Complete | OpenAI prompt refinement, fallback handling, AI-ready parser input documentation, and frontend report section design |
| Week 5 | Complete | Threat timeline wording/evidence rules, sorting/grouping logic, grouped timeline example output, and frontend timeline prototype evidence |

## Timeline

| Done | Dates | Milestone | Scheduled Work |
| --- | --- | --- | --- |
| [x] | June 1-7 | Week 1 | Project kickoff, scope definition, initial requirements, prototype setup |
| [x] | June 8-14 | Week 2 | Data model, sample logs, LLM prompt structure, report/timeline planning |
| [x] | June 15-21 | Week 3 | Log ingestion and parser prototype, parser validation checklist, basic parsed-event review |
| [x] | June 22-28 | Week 4 | OpenAI API integration refinement, structured summarization, backend-to-LLM workflow |
| [x] | June 29-July 5 | Week 5 | Threat timeline generation logic and interactive timeline prototype |
| [x] | July 6-12 | Week 6 | End-to-end report generation and full upload-to-report workflow |
| [ ] | July 13-19 | Week 7 | Integration testing, quality improvement, frontend polish, error handling |
| [ ] | July 20-26 | Week 8 | Final hardening, documentation, demo data, presentation preparation |
| [ ] | July 27-28 | Final Presentation | Final project presentation and live or recorded demonstration |

The timeline above gives a quick project overview. The detailed milestone task plan below breaks the same work into team member responsibilities, outputs, and measurements.

## Project Screenshots

Screenshots should be added to `docs/screenshots/` as the interface is finalized.

Recommended screenshots:

- Flask homepage showing the log input form.
- Sample parsed events or normalized JSON output.
- Example generated report showing summary, risk level, indicators, timeline, evidence, and recommended actions.

## Milestone Task Plan

## Week 1: Project Kickoff and Requirements

**Dates:** June 1-7, 2026  
**Goal:** Define the project scope, responsibilities, tools, and minimum viable prototype.

| Done | Member | Task | Outputs Produced | Measurement |
| --- | --- | --- | --- | --- |
| [x] | Derrick | Confirm project goal and team direction | Initial project concept and team role assignments | Team members understand their responsibilities |
| [x] | Derrick | Create initial prototype framework | Flask app structure, OpenAI API plan, setup instructions, TODO milestones | Prototype can run locally after installing prerequisites |
| [x] | Zion | Identify backend/log processing needs | Initial supported log source list and parser direction | Backend work is aligned with project goal |
| [x] | Oriah | Identify frontend/report needs | Initial report and timeline display expectations | Frontend work is aligned with expected output |

## Week 2: Data Model, Sample Logs, and Output Format

**Dates:** June 8-14, 2026  
**Goal:** Define the shared data structure between backend parsing, LLM summarization, and frontend display.

| Done | Member | Task | Outputs Produced | Measurement |
| --- | --- | --- | --- | --- |
| [x] | Derrick | Draft LLM prompt and output structure | Structured JSON output format for summary, risk, attack type, assets, IOCs, findings, timeline, evidence, and actions | OpenAI output supports the report sections and timeline |
| [x] | Zion | Draft canonical backend event schema | Event schema with timestamp, source, host, user, event type, severity, description, evidence, and raw event | Parser output can support AI summarization and frontend display |
| [x] | Zion | Create sample parser data | Sample CSV security log for parser testing | Team has repeatable test data for Week 3 |
| [x] | Oriah | Plan report and timeline display | Frontend structure based on expected AI output fields | UI can be designed around known report sections |

## Week 3: Log Ingestion and Parser Validation

**Dates:** June 15-21, 2026  
**Goal:** Build and validate the first backend parsing workflow and confirm parser output supports the AI/report structure.

| Done | Member | Task | Outputs Produced | Measurement |
| --- | --- | --- | --- | --- |
| [x] | Derrick | Create parser output validation checklist | `PARSER_OUTPUT_VALIDATION_CHECKLIST.md` with required fields, event types, severity rules, and example JSON | Checklist can be used to review parser output before AI summarization |
| [x] | Derrick | Review parser output against checklist | Feedback for source IP, destination IP, standardized event types, and raw evidence preservation | Parser requirements are clear for backend improvements |
| [x] | Zion | Build first parser prototype | Backend health check and parser execution prototype | Health check returns `status: ok` |
| [x] | Zion | Test parser with sample CSV log | Parser read 4 security events and identified 3 High/Critical events | Parser converts sample logs into normalized JSON |
| [x] | Zion | Generate starter report output | Starter HTML security report with executive summary, validation warnings, and threat timeline table | Backend can produce report-ready output |
| [x] | Oriah | Add basic parsed-event frontend placeholder | Initial browser area for parsed event data and report sections | Frontend can display backend/report fields |

## Week 4: LLM Integration and Structured Summarization

**Dates:** June 22-28, 2026  
**Goal:** Improve the connection between normalized log events and OpenAI summary generation.

| Done | Member | Task | Outputs Produced | Measurement |
| --- | --- | --- | --- | --- |
| [x] | Derrick | Refine OpenAI summarization prompt | Improved prompt instructions for concise, structured security reporting | Model returns consistent JSON sections |
| [x] | Derrick | Improve fallback handling for model output | Clear behavior when model output is invalid or incomplete | App does not crash when output is imperfect |
| [x] | Zion | Connect parser output to AI-ready input | Backend function that sends normalized events to the LLM workflow | Parsed events can be summarized without manual copying |
| [x] | Oriah | Design summary/report sections | Frontend layout for executive summary, risk, findings, timeline, and recommendations | Report output is easy to read in the browser |

## Week 5: Threat Timeline Generation

**Dates:** June 29-July 5, 2026  
**Goal:** Convert parsed and summarized events into a clear chronological threat timeline.

| Done | Member | Task | Outputs Produced | Measurement |
| --- | --- | --- | --- | --- |
| [x] | Derrick | Define timeline event wording and evidence requirements | `docs/week5-timeline-event-requirements.md` with timeline prompt rules and example output | Timeline events include timestamp, source, severity, details, and evidence |
| [x] | Zion | Add sorting and grouping logic | `docs/week5-sorting-grouping-logic.md` and `examples/week5-grouped-timeline.json` | Timeline is ordered and logically grouped |
| [x] | Oriah | Build interactive timeline prototype | Timeline display in HTML/JavaScript and screenshot evidence | User can visually review incident order |

## Week 6: End-to-End Report Generation

**Dates:** July 6-12, 2026  
**Goal:** Connect upload, parsing, summarization, timeline generation, and report rendering into one workflow.

| Done | Member | Task | Outputs Produced | Measurement |
| --- | --- | --- | --- | --- |
| [x] | Derrick | Review report narrative and prompt quality | Improved summary wording, risk rationale, report timestamp, reset workflow, downloadable report output, parsed event preview, and analyst recommendations | Report is clear, consistent, and useful for incident review |
| [x] | Zion | Build backend pipeline from upload to report data | Upload-to-parser-to-summary workflow | User can generate a report from a sample file |
| [x] | Oriah | Build HTML report generator layout | Report sections for summary, findings, IOCs, timeline, and actions | Final report is readable and organized |

## Week 7: Integration Testing and Quality Improvement

**Dates:** July 13-19, 2026  
**Goal:** Test the integrated application and improve reliability, accuracy, and usability.

| Done | Member | Task | Outputs Produced | Measurement |
| --- | --- | --- | --- | --- |
| [x] | Derrick | Improve prompts and summary consistency | `docs/week7-prompt-summary-consistency.md`, `examples/test_logs/`, and updated prompt consistency rules | Summaries are consistent across test logs |
| [x] | Zion | Stabilize integrated application build | `docs/week7-integrated-application-build.md` and `examples/week7-integrated-build-test.json` | Backend evidence covers upload, parsing, normalization, sorting/grouping, report-ready output, and error/correlation checks |
| [ ] | Oriah | Polish timeline and report UI | Cleaner visual layout, labels, and report sections | User can scan the report quickly |

## Week 8: Final Hardening, Documentation, and Presentation Preparation

**Dates:** July 20-26, 2026  
**Goal:** Finalize the demo-ready application, documentation, and presentation materials.

| Done | Member | Task | Outputs Produced | Measurement |
| --- | --- | --- | --- | --- |
| [x] | Derrick | Prepare final README and demo explanation | Updated README, final report draft in `docs/reports/TEAM_FINAL_REPORT.md`, setup guide, project explanation, and demo notes | Instructor can understand the project status and run the prototype |
| [ ] | Zion | Prepare final demo dataset and backend notes | Final sample logs and backend explanation | Demo data works reliably |
| [ ] | Oriah | Prepare presentation visuals and frontend walkthrough | Screenshots, UI explanation, and report/timeline visuals | Presentation clearly shows the user workflow |
| [ ] | Entire Team | Complete final testing | Demo checklist and bug fixes | Project is ready for final presentation |

## Final Presentation and Demonstration

**Dates:** July 27-28, 2026  
**Goal:** Present the completed project and demonstrate the working application.

| Done | Activity | Output | Measurement |
| --- | --- | --- | --- |
| [ ] | Present project problem and motivation | Presentation introduction | Audience understands why security log summarization is useful |
| [ ] | Demonstrate log upload or paste workflow | Live or recorded application demo | User can submit logs and generate a report |
| [ ] | Explain backend parsing and normalization | Backend walkthrough | Audience understands how raw logs become structured events |
| [ ] | Explain OpenAI summarization approach | LLM/prompt walkthrough | Audience understands how summaries and timelines are generated |
| [ ] | Explain frontend timeline/report display | Frontend walkthrough | Audience understands how the report supports incident review |
| [ ] | Discuss testing, limitations, and future work | Test summary and improvement plan | Team can explain current strengths and remaining work |

## Proposed Demo Scenario

**Sample scenario:** SSH brute-force activity followed by a successful root login, suspicious privileged command execution, and firewall blocking of later inbound SSH traffic.

1. User pastes or uploads sample security logs.
2. Backend parser extracts timestamps, hosts, users, IP addresses, event types, severity, evidence, and raw log text.
3. Parser output is checked against the validation checklist.
4. OpenAI summarizes the security activity using the structured project prompt.
5. Application displays executive summary, risk level, attack type, affected assets, indicators of compromise, key findings, timeline events, evidence, and recommended actions.
6. Team explains how the output helps an analyst understand the incident.

## Success Criteria

| Area | Measurement |
| --- | --- |
| Log input | User can paste logs or upload a supported log file |
| Parsing | Parsed output includes timestamp, source, host, user, IP information when available, event type, severity, description, evidence, and raw event |
| LLM output | OpenAI returns structured report data with summary, risk, attack type, assets, IOCs, findings, timeline, evidence, and actions |
| Timeline | Events are displayed chronologically and include supporting evidence |
| Frontend | Browser report is clear, organized, and useful for incident review |
| Testing | Sample security logs are used to test benign and suspicious scenarios |
| Documentation | README explains the project plan, setup, milestones, and current progress |
| Deployment | Prototype can run locally and can be deployed on Windows Server 2025 and Ubuntu 24.04 LTS |
| Final demo | Team can demonstrate the full workflow during the July 27-28 final presentation window |

## Local Setup

### Windows / Windows Server 2025

```powershell
cd C:\Users\redma\Desktop\CapstoneProject
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
notepad .env
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

### Ubuntu 24.04 LTS

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
cd ~/CapstoneProject
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Environment Variables

Create a local `.env` file from `.env.example`.

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=the_model_tested_in_the_openai_api_key_assignment
PORT=5000
```

Do not commit `.env` to GitHub.

## Current Status

As of July 20, 2026:

- Public GitHub repository is active and used for team collaboration.
- Weeks 1-7 core work is documented in the README, milestone checklist, and supporting docs.
- The Flask prototype supports pasted/uploaded logs, structured OpenAI report output, risk rationale, timeline evidence, parsed event preview, reset workflow, and downloadable JSON/HTML reports.
- Derrick's Week 8 final documentation work has started with this README update and the draft final report in `docs/reports/TEAM_FINAL_REPORT.md`.
- Zion's latest backend evidence documents integrated upload, parsing, normalization, sorting/grouping, report-ready JSON, and backend quality checks.
- Oriah's frontend/report planning documents the HTML report sections, field requirements, and visual layout needs.
- Remaining Week 8 work: collect final evidence from Zion and Oriah, complete final demo testing, finish presentation materials, and collect all team signatures before submission.
