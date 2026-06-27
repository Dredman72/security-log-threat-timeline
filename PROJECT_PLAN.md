# Intelligent Security Log Summarization and Threat Timeline Generation

## Project Title

**Intelligent Security Log Summarization and Threat Timeline Generation**

## Team Members and Roles

| Team Member | Role | Primary Responsibilities |
| --- | --- | --- |
| Derrick Redman | Team Leader + AI/LLM Specialist | Overall project coordination, LLM integration, prompt engineering, summarization logic, report quality, final presentation leadership |
| Zion Moore | Backend & Log Processing Lead | Log ingestion, parsing logic, backend workflow, data normalization, error handling, parser testing |
| Oriah Molton-Bowman | Frontend & Visualization Lead | HTML report layout, interactive timeline visualization, user interface flow, frontend polish |

## Project Goal / Objectives

The goal of this capstone project is to build a tool that accepts uploaded security log files and automatically generates a professional HTML report with an interactive threat timeline using the OpenAI API and the model tested in the "Test Your OPENAI API Key" assignment: `gpt-5.4-nano-2026-03-17`.

The system will focus on security analyst usefulness: it should reduce raw log noise, identify meaningful events, summarize activity in clear language, and place events into a timeline that helps explain what happened during a potential security incident.

### Objectives

- Accept uploaded security log files, including Windows Event Logs, Sysmon logs, firewall logs, and EDR-style logs where possible.
- Parse and normalize log entries into a consistent internal event format.
- Use the OpenAI API with `gpt-5.4-nano-2026-03-17` to summarize security-relevant activity.
- Generate a threat timeline that orders key events by time and highlights important context.
- Produce a clean HTML report suitable for review by a security analyst, instructor, or project evaluator.
- Provide a working demo by the final presentation dates of **July 27-28, 2026**.

## Detailed Weekly Timeline

### Week 1: June 1 - June 7, 2026

**Focus:** Project kickoff, scope definition, and requirements.

| Deliverable | Owner |
| --- | --- |
| Confirmed project scope and success criteria | Derrick |
| Initial list of supported log sources | Zion |
| Initial frontend/report expectations | Oriah |

**Tasks:**

- Hold project kickoff meeting and confirm each team member's responsibilities.
- Define the minimum viable product for the capstone demo.
- Identify target log types: Windows Event Logs, Sysmon, firewall, and EDR-style logs.
- Decide whether the first working version will use Streamlit or Flask.
- Create an initial project folder structure and planning documents.

### Week 2: June 8 - June 14, 2026

**Focus:** Data model, sample logs, and architecture.

| Deliverable | Owner |
| --- | --- |
| Canonical event schema draft | Zion |
| LLM prompt and output structure draft | Derrick |
| Timeline/report wireframe | Oriah |

**Tasks:**

- Collect or create sample logs for testing.
- Define the normalized event format, including fields such as timestamp, source, host, user, event type, severity, description, raw event, and evidence.
- Draft the LLM prompt structure for event summarization and timeline generation.
- Sketch the report layout and timeline interaction flow.
- Confirm the backend-to-frontend data contract.

**Week 2 Accomplishments:**

- Zion completed the canonical backend event schema draft for parsed security logs.
- Zion's schema defines key parser fields including timestamp, source, host, user, event type, severity, description, evidence, and raw event.
- Zion created a sample CSV security log for parser testing, preparing the backend work for Week 3.
- Derrick completed the OpenAI LLM prompt and structured JSON output format draft, including executive summary, risk level, attack type, affected assets, indicators of compromise, key findings, timeline events with evidence, and recommended actions.
- The backend schema and OpenAI output structure now align around shared fields that support the AI summarization prompt and frontend timeline/report display.

### Week 3: June 15 - June 21, 2026

**Focus:** Log ingestion and parsing prototype.

| Deliverable | Owner |
| --- | --- |
| Working upload/ingestion prototype | Zion |
| Parser output validation checklist | Derrick |
| Basic frontend placeholder for parsed events | Oriah |

Derrick's parser output validation checklist is documented in `PARSER_OUTPUT_VALIDATION_CHECKLIST.md`. The checklist defines required parsed event fields, recommended event types, severity rules, example JSON output, and validation criteria for reviewing parser output before it is sent to OpenAI.

**Tasks:**

- Implement initial parsing for at least one primary log format.
- Convert parsed records into the canonical event schema.
- Add basic validation for missing timestamps, malformed rows, and unsupported file types.
- Build a simple view that can display parsed event data.
- Review parsed output for usefulness and accuracy.

**Week 3 Accomplishments:**

- Zion completed the first backend parsing prototype and verified the backend health check returned `status: ok`.
- Zion tested the parser with the sample CSV security log and confirmed it parsed 4 security events.
- Zion identified 3 High/Critical events from the parsed sample data.
- Zion generated normalized JSON output using the canonical event schema.
- Zion generated a starter HTML security report with an executive summary, validation warnings, and a threat timeline table.
- Derrick completed `PARSER_OUTPUT_VALIDATION_CHECKLIST.md` and used it to review Zion's parser output.
- Derrick's review confirmed Zion's parser output includes the major checklist fields and recommended adding `source_ip` and `destination_ip` when available, standardizing event type names, and preserving the original CSV row or raw log line in `raw_event`.
- Oriah's focus was on creating the foundation for the frontend display of parsed security events.
- Oriah received sample parser output from Zion and reviewed the data to make sure it matched the fields from the Week 2 report and timeline wireframe. The sample data included important event fields such as `timestamp`, `source`, `host`, `user`, `event_type`, `severity`, `description`, `evidence`, and `raw_event`. This helped confirm that the backend parser output can support the frontend report and timeline design.
- Oriah completed the Week 3 task by using Zion’s parsed event sample to plan the basic frontend placeholder for displaying security events. The data can be shown in a table, event card layout, or timeline-style view.

**Evidence to include:** screenshot of Zion’s JSON parser output and screenshot/mockup of the parsed event display layout.

### Week 4: June 22 - June 28, 2026

**Focus:** LLM integration and structured summarization.

| Deliverable | Owner |
| --- | --- |
| OpenAI API integration prototype | Derrick |
| Backend function for sending normalized events to the LLM | Zion |
| Report section design for summary output | Oriah |

**Tasks:**

- Connect the backend to the OpenAI API using the model tested in the "Test Your OPENAI API Key" assignment.
- Build prompts for concise incident summaries, notable events, and security analyst recommendations.
- Require structured LLM output where practical, such as JSON sections for summary, timeline events, indicators, and recommendations.
- Add fallback behavior for invalid or incomplete LLM responses.
- Test summarization against sample logs and revise prompts.

**Week 4 Accomplishments:**

- Derrick refined the OpenAI summarization prompt so the model is instructed to return concise, structured JSON report output.
- Derrick strengthened the expected report structure for executive summary, risk level, attack type, affected assets, indicators of compromise, key findings, timeline evidence, and recommended actions.
- Derrick improved fallback handling so the app cleans common JSON formatting issues, fills safe defaults for missing fields, and does not crash when model output is incomplete or invalid.
- Derrick updated upload handling and error messaging so unsupported files, raw `.evtx` files, and oversized uploads return clear user-facing messages.
- Zion completed the Week 4 AI-ready parser input documentation in `docs/week4-ai-ready-parser-input.md`.
- Zion provided `examples/ai-ready-parser-input.json`, showing how normalized parsed events can be structured before being sent into the OpenAI summarization workflow.
- Zion's Week 4 work confirms that parsed events can be summarized without manually copying each event into the LLM workflow.
- Oriah's Week 4 frontend report section design remains the next item needed to finish the full Week 4 team milestone.
- Oriah reviewed the OpenAI-generated report output and the normalized JSON event data uploaded by the team. Her focus was on the frontend/report design for the AI summary output.
- Oriah confirmed that the report includes the major sections needed for the project: report summary, risk level, assets and indicators, key findings, threat timeline, and recommended actions.
- Oriah can use the OpenAI report output screenshots showing the report summary, key findings, threat timeline, and recommended actions. These screenshots show that the AI-generated content can be organized into the report sections she designed.
- Oriah's contribution was reviewing the AI report output, confirming that the report sections match the frontend design plan, and identifying how the summary output should be displayed for users.

### Week 5: June 29 - July 5, 2026

**Focus:** Threat timeline generation.

| Deliverable | Owner |
| --- | --- |
| Timeline event generation logic | Derrick |
| Backend sorting/grouping logic | Zion |
| Interactive timeline prototype | Oriah |

**Tasks:**

- Convert normalized events and LLM summaries into timeline entries.
- Sort timeline events chronologically.
- Group related events by host, user, process, IP address, or event type where possible.
- Assign severity labels such as Low, Medium, High, and Critical.
- Build the first interactive timeline view in HTML and JavaScript.

### Week 6: July 6 - July 12, 2026

**Focus:** End-to-end report generation.

| Deliverable | Owner |
| --- | --- |
| HTML report generator | Oriah |
| Backend pipeline from upload to report data | Zion |
| Report narrative review and prompt improvements | Derrick |

**Tasks:**

- Connect upload, parsing, summarization, timeline generation, and report rendering into one workflow.
- Add report sections for executive summary, key findings, timeline, indicators, and recommendations.
- Improve report readability and formatting.
- Test the full flow with multiple sample log files.
- Document known limitations and unsupported log formats.

### Week 7: July 13 - July 19, 2026

**Focus:** Integration testing, quality improvement, and correlation.

| Deliverable | Owner |
| --- | --- |
| Integrated application build | Zion |
| Improved prompts and summary consistency | Derrick |
| Polished timeline and report UI | Oriah |

**Tasks:**

- Test the tool with realistic security scenarios.
- Improve event correlation across multiple logs.
- Add clear error messages for upload, parsing, and LLM failures.
- Refine timeline filtering or labels if time allows.
- Review generated reports for accuracy, clarity, and professional tone.

### Week 8: July 20 - July 26, 2026

**Focus:** Final hardening, documentation, and presentation preparation.

| Deliverable | Owner |
| --- | --- |
| Final demo-ready application | Entire team |
| Final README and usage instructions | Derrick |
| Demo dataset and presentation visuals | Zion and Oriah |

**Tasks:**

- Freeze major features and focus on reliability.
- Complete final testing using the planned demo dataset.
- Fix priority bugs and remove confusing UI behavior.
- Prepare final presentation slides and demo script.
- Confirm that the final report output is clean, readable, and ready to present.

### Week 9: July 27 - July 28, 2026

**Focus:** Final presentation and submission.

| Deliverable | Owner |
| --- | --- |
| Final capstone presentation | Derrick |
| Live or recorded application demo | Entire team |
| Final project submission package | Entire team |

**Tasks:**

- Present the project during the final presentation window.
- Demonstrate uploading logs and generating a threat timeline report.
- Explain the backend parsing workflow, LLM summarization approach, and frontend visualization.
- Submit final source code, documentation, report examples, and presentation materials.

## Major Milestones

| Milestone | Target Date | Owner | Success Indicator |
| --- | --- | --- | --- |
| Requirements and scope finalized | June 7, 2026 | Derrick | Team agrees on MVP, supported logs, and success criteria |
| Canonical event schema completed | June 14, 2026 | Zion | Parsed logs can be represented in one consistent format |
| Parsing prototype working | June 21, 2026 | Zion | At least one log type can be uploaded, parsed, and displayed |
| LLM summarization prototype working | June 28, 2026 | Derrick | OpenAI returns useful summaries from normalized events using the tested assignment model |
| Interactive timeline prototype completed | July 5, 2026 | Oriah | Timeline displays ordered security events in the browser |
| End-to-end report generation completed | July 12, 2026 | Entire team | Upload-to-report workflow works with sample data |
| Integrated demo build completed | July 19, 2026 | Entire team | Application is stable enough for full practice demos |
| Final demo package completed | July 26, 2026 | Entire team | Slides, README, demo data, and final application are ready |
| Final presentation delivered | July 27-28, 2026 | Entire team | Project is presented and submitted successfully |

## Final Deliverables

- Working application using Python with either Streamlit or Flask.
- Log upload and ingestion workflow.
- Parser or normalization logic for supported security log formats.
- OpenAI API integration for summarization and timeline generation.
- Interactive HTML/JavaScript threat timeline.
- Generated HTML report with security summary, key findings, timeline, and recommendations.
- Sample input logs used for testing and demonstration.
- README with setup, usage instructions, system overview, and known limitations.
- Final presentation slides.
- Demo script or recorded walkthrough, if required.

## Acceptance Criteria

The project will be considered successful if the following criteria are met:

- A user can upload at least one supported security log file through the application.
- The system parses the uploaded log into structured event data.
- Parsed events include useful fields such as timestamp, event source, event description, severity or category, and supporting evidence.
- The application successfully sends normalized event data to the OpenAI API for summarization using the tested assignment model.
- The generated summary is readable, relevant, and focused on security analyst needs.
- The application generates a chronological threat timeline from the parsed and summarized events.
- The timeline is interactive or visually organized enough to support incident review.
- The final HTML report includes an executive-style summary, key findings, threat timeline, and recommendations.
- The end-to-end workflow can be demonstrated during the July 27-28 final presentation window.
- The final repository includes enough documentation for an instructor or evaluator to understand how to run and review the project.

## Scope Notes

The minimum viable product is a reliable upload-to-report workflow for one or more representative security log formats. Advanced multi-source correlation, external enrichment, and broad EDR support are valuable stretch goals, but they should not delay the core demo-ready workflow.
