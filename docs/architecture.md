# Architecture

Course Materials Ops Agent is a local-first ADK agent that turns a messy course
workspace into a grounded operational assistant.

## Goals

- Answer course and capstone status questions from local source files.
- Return official links already recorded in the workspace.
- Separate completed work, pending human actions, and optional cloud tasks.
- Refuse secret access and unsafe deployment claims.

## Components

```text
User
  |
  v
ADK Agent: app/agent.py
  |
  +--> list_allowed_course_files()
  +--> read_course_file()
  +--> list_official_links()
  +--> get_course_status()
  +--> search_course_notes()
  +--> check_deployment_readiness()
  +--> prepare_capstone_summary()
  |
  v
Whitelisted local files
  - notes/course-log.md
  - notes/link-log.md
  - work/day-*/material-notes.md
  - work/day-05/production-checklist.md
  - capstone/*.md
  - submissions/*.md
  - capstone/course-ops-agent/docs/*.md
```

Workspace root resolution order:

1. `COURSE_WORKSPACE_ROOT`, if set.
2. The nearest parent directory containing `notes/link-log.md` and
   `capstone/spec.md`.
3. The bundled sanitized `demo_workspace/`.

## Trust Boundaries

The LLM can decide which tool to call, but file access is enforced by
deterministic Python code before content reaches the model.

Secret boundaries:

- `.env` is blocked by path checks.
- `.kaggle` is blocked by path checks.
- Search queries containing `.env` or `secret` are refused.
- Real cloud deployment is blocked unless prerequisites and explicit approval
  are recorded.

## Data Flow

1. The user asks a course, capstone, or deployment question.
2. The agent chooses a local tool.
3. The tool validates the path/query/action against allowlists and safety rules.
4. The tool returns concise, source-labeled data.
5. The agent answers in the user's language and separates completed vs pending
   work.

## Why Local-First

The capstone problem is operational correctness rather than raw generation. A
local-first design keeps answers auditable, avoids unnecessary billing risk, and
lets the user prepare a Kaggle submission without deploying cloud resources.

## Extension Points

- Add a small web UI for a public demo.
- Add MCP to expose the course workspace as a local resource server.
- Add managed eval traces once Google Cloud ADC is intentionally configured.
- Add Agent Runtime or Cloud Run deployment only after dry-run review and user
  approval.
