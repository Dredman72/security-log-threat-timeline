# Milestone TODOs

**Project:** Intelligent Security Log Summarization and Threat Timeline Generation  
**Course:** CSC 482 Capstone Project 2  
**Team:** Derrick Redman, Zion Moore, Oriah Molton-Bowman  
**Planning Window:** June 1-July 28, 2026

This file tracks the team's weekly milestones, task ownership, and progress. It should be updated each week as work is completed and pushed to the GitHub repository.

## Quick Timeline

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

## Week 1: Project Kickoff and Requirements

**Dates:** June 1-7, 2026  
**Goal:** Define the project scope, responsibilities, tools, and minimum viable prototype.

| Done | Member | Task | Output | Measurement |
| --- | --- | --- | --- | --- |
| [x] | Derrick | Create initial prototype framework | Flask app structure, OpenAI API plan, setup instructions, TODO milestones | Prototype can run locally after installing prerequisites |
| [x] | Zion | Identify backend/log processing needs | Initial supported log source list and parser direction | Backend work is aligned with project goal |
| [x] | Oriah | Identify frontend/report needs | Initial report and timeline display expectations | Frontend work is aligned with expected output |

## Week 2: Data Model, Sample Logs, and Output Format

**Dates:** June 8-14, 2026  
**Goal:** Define the shared data structure between backend parsing, LLM summarization, and frontend display.

| Done | Member | Task | Output | Measurement |
| --- | --- | --- | --- | --- |
| [x] | Derrick | Draft LLM prompt and output structure | Structured JSON output format for summary, risk, attack type, assets, IOCs, findings, timeline, evidence, and actions | OpenAI output supports the report sections and timeline |
| [x] | Zion | Draft canonical backend event schema | Event schema with timestamp, source, host, user, event type, severity, description, evidence, and raw event | Parser output can support AI summarization and frontend display |
| [x] | Zion | Create sample parser data | Sample CSV security log for parser testing | Team has repeatable test data for Week 3 |
| [x] | Oriah | Plan report and timeline display | Frontend structure based on expected AI output fields | UI can be designed around known report sections |

## Week 3: Log Ingestion and Parser Validation

**Dates:** June 15-21, 2026  
**Goal:** Build and validate the first backend parsing workflow and confirm parser output supports the AI/report structure.

| Done | Member | Task | Output | Measurement |
| --- | --- | --- | --- | --- |
| [x] | Derrick | Create parser output validation checklist | `PARSER_OUTPUT_VALIDATION_CHECKLIST.md` | Checklist confirms parser fields support LLM output and frontend display |
| [x] | Zion | Build first parser prototype | Parser reads sample CSV security log | Parser reads test events successfully |
| [x] | Zion | Generate normalized JSON output | Parsed events converted into canonical event schema | Output includes timestamp, source, host, user, event type, severity, description, evidence, and raw event |
| [x] | Zion | Generate starter report output | Starter HTML security report with executive summary, validation warnings, and threat timeline table | Backend can produce report-ready output |
| [x] | Oriah | Add basic parsed-event frontend placeholder | Initial browser area for parsed event data and report sections | Frontend can display backend/report fields |

## Week 4: LLM Integration and Structured Summarization

**Dates:** June 22-28, 2026  
**Goal:** Improve the connection between normalized log events and OpenAI summary generation.

| Done | Member | Task | Output | Measurement |
| --- | --- | --- | --- | --- |
| [x] | Derrick | Refine OpenAI prompt and structured output | Improved prompt for consistent JSON report output | Output reliably includes summary, risk, attack type, assets, IOCs, findings, timeline, evidence, and actions |
| [x] | Derrick | Add or review fallback behavior | Graceful response when OpenAI output is incomplete or invalid JSON | App does not fail silently when model output needs cleanup |
| [x] | Zion | Connect parser output to AI input format | Normalized event data ready for LLM summarization | Parser output can be passed into the LLM workflow |
| [x] | Oriah | Design summary/report sections | Frontend layout for executive summary, risk, findings, timeline, and recommendations | Report output is easy to read in the browser |

## Week 5: Threat Timeline Generation

**Dates:** June 29-July 5, 2026  
**Goal:** Convert parsed and summarized events into a clear chronological threat timeline.

| Done | Member | Task | Output | Measurement |
| --- | --- | --- | --- | --- |
| [x] | Derrick | Define timeline event wording and evidence requirements | `docs/week5-timeline-event-requirements.md` with timeline prompt rules and example output | Timeline events include timestamp, source, severity, details, and evidence |
| [x] | Zion | Add sorting and grouping logic | `docs/week5-sorting-grouping-logic.md` and `examples/week5-grouped-timeline.json` | Timeline is ordered and logically grouped |
| [x] | Oriah | Build interactive timeline prototype | Timeline display in HTML/JavaScript | User can visually review incident order |

## Week 6: End-to-End Report Generation

**Dates:** July 6-12, 2026  
**Goal:** Connect upload, parsing, summarization, timeline generation, and report rendering into one workflow.

| Done | Member | Task | Output | Measurement |
| --- | --- | --- | --- | --- |
| [x] | Derrick | Review report narrative and prompt quality | Improved summary wording, risk rationale, report timestamp, reset workflow, downloadable report output, parsed event preview, and analyst recommendations | Report is clear, consistent, and useful for incident review |
| [x] | Zion | Connect upload, parser, and normalized output | Backend flow from uploaded file to normalized events | Uploaded sample logs are parsed correctly |
| [x] | Oriah | Build HTML report generator layout | Report sections for summary, findings, IOCs, timeline, and actions | Final report is readable and organized |

## Week 7: Integration Testing and Quality Improvement

**Dates:** July 13-19, 2026  
**Goal:** Test the integrated application and improve reliability, accuracy, and usability.

| Done | Member | Task | Output | Measurement |
| --- | --- | --- | --- | --- |
| [x] | Derrick | Test OpenAI summaries against sample scenarios | `docs/week7-prompt-summary-consistency.md`, `examples/test_logs/`, and updated prompt consistency rules | Summaries are accurate, clear, and useful |
| [x] | Zion | Test parser with multiple log samples | `docs/week7-integrated-application-build.md` and `examples/week7-integrated-build-test.json` | Backend evidence covers upload, parsing, normalization, grouping, report-ready output, and error/correlation checks |
| [ ] | Oriah | Polish timeline and report UI | Cleaner visual layout, labels, and report sections | User can scan the report quickly |

## Week 8: Final Hardening, Documentation, and Presentation Preparation

**Dates:** July 20-26, 2026  
**Goal:** Finalize the demo-ready application, documentation, and presentation materials.

| Done | Member | Task | Output | Measurement |
| --- | --- | --- | --- | --- |
| [x] | Derrick | Finalize README, prompt notes, and demo explanation | Updated README, final report draft, documentation, and AI workflow explanation | Instructor can understand how the LLM is used and how to run/review the prototype |
| [ ] | Zion | Prepare parser/backend walkthrough | Backend explanation and sample parser output | Team can explain how logs are normalized |
| [ ] | Oriah | Prepare presentation visuals and frontend walkthrough | Screenshots, UI explanation, and report/timeline visuals | Presentation clearly shows the user workflow |
| [ ] | Entire Team | Complete final testing | Demo checklist and bug fixes | Project is ready for final presentation |

## Final Presentation and Demonstration

**Dates:** July 27-28, 2026  
**Goal:** Present the final project and demonstrate the working prototype.

| Done | Activity | Output | Measurement |
| --- | --- | --- | --- |
| [ ] | Present project problem and motivation | Presentation introduction | Audience understands the project purpose |
| [ ] | Demonstrate upload/paste log workflow | Live or recorded demo | User can see logs being submitted |
| [ ] | Demonstrate OpenAI summarization output | Generated report | Audience can see summary, risk, findings, timeline, and recommendations |
| [ ] | Explain backend parser workflow | Backend walkthrough | Audience understands how raw logs become structured events |
| [ ] | Explain frontend timeline/report display | Frontend walkthrough | Audience understands how the report supports incident review |
| [ ] | Discuss testing, limitations, and future work | Test summary and improvement plan | Team can explain current strengths and remaining work |

## Weekly Update Instructions

Each week, update this file by:

1. Changing completed tasks from `[ ]` to `[x]`.
2. Adding short notes if a task changed or moved to another week.
3. Keeping task descriptions consistent with `README.md` and `PROJECT_PLAN.md`.
4. Committing the update to GitHub with a clear message, such as `Update milestone TODOs for Week 4`.
