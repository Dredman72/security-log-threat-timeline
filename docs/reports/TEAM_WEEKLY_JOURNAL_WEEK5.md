# Team Weekly Journal - Week 5

**Project:** Intelligent Security Log Summarization and Threat Timeline Generation  
**Course:** CSC 482 Capstone Project 2  
**Team:** Project Team 2  
**Team Members:** Derrick Redman, Zion Moore, Oriah Molton-Bowman  
**Week:** Week 5, June 29-July 5, 2026  
**GitHub Repository:** https://github.com/Dredman72/security-log-threat-timeline

## Milestones Achieved

### Milestone 1: Threat Timeline Requirements Defined

The team advanced the Week 5 goal of threat timeline generation by defining how timeline events should be written and what evidence must be included. Derrick completed the timeline wording and evidence requirements so the OpenAI prompt, backend parser output, and frontend timeline display can all follow the same structure.

The timeline requirements define that every timeline event should include a timestamp, source, short event title, severity, details, and evidence. This helps make the final report useful for incident review because each event can be traced back to a specific log detail.

### Milestone 2: Sorting and Grouping Logic Documented

Zion completed the Week 5 backend sorting and grouping documentation. This work explains how parsed events should be sorted chronologically and grouped by useful investigation fields such as host, user, source IP, destination IP, event type, and severity.

This supports the final timeline because the report needs to show events in the order they happened while also helping analysts identify repeated activity from the same host, user, or IP address.

### Milestone 3: Week 5 Progress Tracking Updated

The team updated the README and milestone tracking files so the repository reflects the current Week 5 status. Week 4 is now marked complete, Derrick's Week 5 timeline requirements task is marked complete, Zion's Week 5 sorting/grouping task is marked complete, and Oriah's Week 5 interactive timeline prototype remains pending until submitted.

## Subtasks Completed

| Member | Subtask | Brief Description |
| --- | --- | --- |
| Derrick | Defined timeline event wording rules | Created clear rules for how timeline event titles and details should be written so the output is specific, evidence-based, and easy to read. |
| Derrick | Defined timeline evidence requirements | Documented that each timeline event must include supporting evidence such as a log line, event ID, IP address, username, command, process, file path, or alert name. |
| Derrick | Updated OpenAI prompt direction | The application prompt was tightened so timeline events must include timestamp, source, severity, details, and evidence. |
| Derrick | Updated project tracking | Updated README and milestone status to show Week 4 complete and current Week 5 progress. |
| Zion | Documented chronological sorting logic | Added documentation explaining that events should be sorted by timestamp from oldest to newest. |
| Zion | Documented grouping logic | Added grouping fields for host, user, source IP, destination IP, event type, and severity. |
| Zion | Added grouped timeline example | Added an example grouped timeline JSON file to show how sorted/grouped timeline output can look. |
| Oriah | Interactive timeline prototype | Pending. Oriah still needs to submit or push the Week 5 interactive timeline prototype evidence. |

## Testing of Subtasks With Evidence

### Test 1: Timeline Requirements Review

**Purpose:** Confirm Derrick's timeline requirements define the fields needed for a usable threat timeline.  
**Procedure:** The team reviewed `docs/week5-timeline-event-requirements.md`.  
**Expected Result:** The document should define required timeline fields and include example output.  
**Result:** Passed. The document defines timestamp, source, event, severity, details, and evidence requirements, plus example timeline JSON.

**Screenshot Evidence:** Insert screenshot of `docs/week5-timeline-event-requirements.md`.

### Test 2: OpenAI Prompt Timeline Rules Review

**Purpose:** Confirm the Flask/OpenAI prompt supports the Week 5 timeline requirements.  
**Procedure:** Derrick reviewed the prompt in `app.py` after updating the timeline wording and evidence rules.  
**Expected Result:** The prompt should tell OpenAI to return timeline events with timestamp, source, event, severity, details, and evidence.  
**Result:** Passed. The prompt now includes stronger rules for timeline titles, details, and evidence.

**Screenshot Evidence:** Insert screenshot of the Week 5 prompt rules in `app.py`.

### Test 3: Sorting and Grouping Logic Review

**Purpose:** Confirm Zion's backend timeline organization work supports chronological timeline generation.  
**Procedure:** The team reviewed `docs/week5-sorting-grouping-logic.md`.  
**Expected Result:** The document should explain sorting by timestamp and grouping by investigation fields.  
**Result:** Passed. The document explains sorting by timestamp and grouping by host, user, source IP, destination IP, event type, and severity.

**Screenshot Evidence:** Insert screenshot of `docs/week5-sorting-grouping-logic.md`.

### Test 4: Grouped Timeline JSON Review

**Purpose:** Confirm Zion provided example output for grouped timeline data.  
**Procedure:** The team reviewed `examples/week5-grouped-timeline.json`.  
**Expected Result:** The example should show timeline events in timestamp order and provide grouped counts.  
**Result:** Passed. The example includes a `timeline_summary`, chronological `timeline` events, and grouped counts by host, user, source IP, destination IP, event type, and severity.

**Screenshot Evidence:** Insert screenshot of `examples/week5-grouped-timeline.json`.

### Test 5: Milestone Tracker Review

**Purpose:** Confirm the repository status matches the actual Week 5 work completed.  
**Procedure:** Derrick reviewed and updated `README.md` and `MILESTONE_TODOS.md`.  
**Expected Result:** Week 4 should be marked complete, Derrick and Zion should be marked complete for Week 5, and Oriah should remain pending until her timeline prototype is submitted.  
**Result:** Passed. The tracking files now reflect the current Week 5 status.

**Screenshot Evidence:** Insert screenshot of the Week 5 section in `MILESTONE_TODOS.md`.

## Lessons Learned

- The team learned that timeline generation is more than listing events. Each event needs clear wording, severity, and evidence so the report can support incident review.
- Derrick learned that the LLM prompt needs explicit timeline rules so the model does not return vague event descriptions.
- Zion's sorting and grouping work showed that chronological ordering and grouping fields are important for finding patterns across logs.
- The team learned that project tracking files must be updated after each role submits work, otherwise GitHub may contain completed files while the checklist still shows the task as incomplete.
- The team also learned that frontend timeline work depends on both Derrick's timeline wording rules and Zion's sorted/grouped event structure.

## Contribution of Each Team Member

| Team Member | Role | Week 5 Contribution |
| --- | --- | --- |
| Derrick Redman | Team Leader + AI/LLM Specialist | Completed the Week 5 timeline event wording and evidence requirements, updated the OpenAI prompt rules for timeline output, reviewed current team progress, and updated README/milestone status. |
| Zion Moore | Backend & Log Processing Lead | Completed Week 5 sorting and grouping logic documentation and added an example grouped timeline JSON file showing chronological events and grouped counts. |
| Oriah Molton-Bowman | Frontend & Visualization Lead | Week 5 interactive timeline prototype is still pending based on the local repository files currently available. Her next step is to submit or push the interactive timeline prototype and screenshot evidence. |

## Progress Compared to Project Plan

The team has progressed according to the Week 5 plan for Derrick and Zion's responsibilities. Derrick completed the timeline event wording and evidence requirements. Zion completed the sorting and grouping logic documentation with example grouped timeline output.

Week 5 is not fully complete yet because Oriah's interactive timeline prototype still needs to be submitted or pushed to the shared repository. Until that is complete, the overall Week 5 milestone should remain in progress.

## Plan Adjustment

No major project plan adjustment is needed. The team will continue with the current Flask/HTML direction.

The immediate adjustment is to follow up with Oriah for her Week 5 interactive timeline prototype. Once Oriah submits that work, the team should update `MILESTONE_TODOS.md`, update the README, add screenshot evidence, and mark Week 5 complete.

## Next Steps

| Owner | Next Step |
| --- | --- |
| Derrick | Review Oriah's timeline prototype once submitted and confirm it matches the timeline wording/evidence requirements. |
| Zion | Be ready to support the frontend with sorted/grouped timeline data if Oriah needs backend sample data. |
| Oriah | Submit or push the interactive timeline prototype and provide screenshot evidence. |
| Entire Team | Prepare Week 5 evidence screenshots and keep the GitHub repository updated. |

## Team Sign-Off

Each team member should sign before submission.

| Team Member | Role | Signature | Date |
| --- | --- | --- | --- |
| Derrick Redman | Team Leader + AI/LLM Specialist |  |  |
| Zion Moore | Backend & Log Processing Lead |  |  |
| Oriah Molton-Bowman | Frontend & Visualization Lead |  |  |
