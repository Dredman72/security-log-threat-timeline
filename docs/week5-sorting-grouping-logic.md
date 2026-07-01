# Week 5: Sorting and Grouping Logic

## Goal

Convert parsed and normalized security events into a clear chronological threat timeline.

## Zion's Task

Add sorting and grouping logic so parsed events can be organized by timestamp and grouped by useful investigation fields.

## Sorting Logic

Events are sorted by the `timestamp` field from oldest to newest. This allows the report to show the order of activity as it happened.

## Grouping Logic

Events can be grouped by:

- `host`
- `user`
- `source_ip`
- `destination_ip`
- `event_type`
- `severity`

## Why This Matters

Chronological sorting helps analysts understand the sequence of suspicious activity. Grouping helps identify patterns, such as repeated activity from the same host, user, IP address, severity level, or event type.

## Example Workflow

1. Start with normalized parser output.
2. Validate required event fields.
3. Sort events by timestamp.
4. Group events by investigation field.
5. Send the organized timeline to the report view.

## Example Output

See:

`examples/week5-grouped-timeline.json`

## Measurement

The timeline output can show parsed security events in chronological order and summarize grouped activity by host, user, IP address, event type, and severity.

## Status

Completed for Week 5.