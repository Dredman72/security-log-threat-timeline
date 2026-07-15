# Week 7: Integrated Application Build

## Owner

Zion Moore

## Focus

Integration testing, quality improvement, and correlation.

## Goal

Verify that the backend pieces of the application work together as one integrated workflow.

## Integrated Workflow

The Week 7 integrated application build connects:

1. File upload
2. Log parsing
3. Event normalization
4. Event sorting and grouping
5. Report-ready data generation
6. Timeline/report output

## Testing Scenarios

The application should be tested with realistic security scenarios, including:

- Suspicious PowerShell execution
- Firewall block events
- Multiple failed login attempts
- Malware or ransomware alert behavior
- Mixed severity events
- Multiple users or hosts

## Quality Improvements

Week 7 integration review checks for:

- Clear parser output
- Consistent event field names
- Chronological event ordering
- Grouped event counts
- Report-ready JSON structure
- Clear error messages for missing or invalid files
- Report language that is clear and professional

## Error Handling Checks

The integrated build should provide clear messages for:

- Missing uploaded file
- Unsupported file type
- Empty log file
- Malformed event data
- Parser failure
- LLM/API summary failure

## Correlation Checks

The backend should support correlation across:

- `host`
- `user`
- `source_ip`
- `destination_ip`
- `event_type`
- `severity`

## Expected Result

A user can upload a sample security log file and generate report-ready data without manually copying parser output between steps.

## Status

Completed for Week 7 integration testing evidence.