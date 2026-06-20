# Capstone Spec - Course Materials Ops Agent

## Overview

Course Materials Ops Agent is a local-first AI course operations assistant. It
answers questions about course status, official links, capstone readiness, and
deployment blockers using only whitelisted local files.

## Problem

Fast-moving course work creates scattered state across daily assignments,
codelabs, videos, badge pages, local prototypes, and optional cloud tasks. The
agent helps avoid stale or overconfident answers by grounding responses in
recorded notes.

## Users

- Primary user: a course participant preparing the Kaggle capstone submission.
- Secondary user: a reviewer checking what the project does and how it behaves.

## Example Use Cases

1. `What is left for Day 5?`
2. `Which official links do we have for Day 4 and Day 5?`
3. `Can we deploy now?`
4. `Prepare my capstone summary.`

## Safety Rules

- Never read or print `.env` values.
- Never claim deployment unless local notes prove it.
- Never run cloud deployment without explicit user approval.
- Prefer official links recorded in `notes/link-log.md`.

## Success Criteria

- The agent identifies the Kaggle capstone submission requirements.
- The agent returns official Day 4 and Day 5 links.
- The agent blocks real cloud deployment until prerequisites are met.
- The agent separates completed, pending, and human-owned work.
