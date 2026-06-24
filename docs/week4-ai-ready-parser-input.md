# Week 4: AI-Ready Parser Input

## Goal

Connect normalized parser output to the LLM summary workflow.

## What This Adds

This documentation shows how parsed security log events can be structured before being sent into the AI summarization step.

## AI-Ready Input Fields

Each event includes:

- `timestamp`
- `source`
- `host`
- `user`
- `event_type`
- `severity`
- `description`
- `evidence`

## Example File

See:

`examples/ai-ready-parser-input.json`

## Measurement

Parsed events can be summarized without manually copying each event into the LLM workflow.

## Status

Completed for Week 4.