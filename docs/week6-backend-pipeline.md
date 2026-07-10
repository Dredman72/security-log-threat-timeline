# Week 6: Backend Upload-to-Report Pipeline

## Goal

Connect upload, parsing, summarization, timeline generation, and report rendering into one backend workflow.

## Zion's Task

Build and document the backend pipeline from uploaded sample file to report-ready data.

## Pipeline Steps

1. User uploads a sample security log file.
2. Backend receives the uploaded file.
3. Parser reads the file and extracts security events.
4. Events are normalized into a consistent JSON structure.
5. Normalized events are sorted into chronological order.
6. Events are grouped by investigation fields such as host, user, source IP, destination IP, event type, and severity.
7. Summary and timeline data are prepared for report rendering.
8. Report-ready data is passed to the frontend/report template.

## Backend Workflow

```text
Upload File
   ↓
Parse Log File
   ↓
Normalize Events
   ↓
Sort Events By Timestamp
   ↓
Group Events By Investigation Field
   ↓
Prepare Summary + Timeline Data
   ↓
Render Report