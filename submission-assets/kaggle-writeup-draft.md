# Course Materials Ops Agent

Subtitle: A local-first agent that keeps a fast-moving AI course workspace grounded, safe, and submission-ready.

Track to select in Kaggle UI: choose the closest track for productivity, developer tooling, or workflow automation after joining the capstone competition.

## Summary

Course Materials Ops Agent is a local-first AI assistant for managing the Kaggle 5-Day AI Agents: Intensive Vibe Coding Course workspace. The project solves a practical problem I ran into during the course: materials, codelabs, official links, badge pages, local agent prototypes, API credentials, and optional cloud tasks all move quickly, and it is easy to lose track of what is actually done.

The agent answers questions such as:

- What is left for Day 5?
- Which official links do we have for Day 4 and Day 5?
- Can we deploy the capstone to Google Cloud now?
- Prepare a short capstone summary.

The important design choice is that the agent does not simply "remember" course status from the prompt. It uses deterministic tools over a whitelisted local workspace, reads source files such as course logs and link logs, and refuses unsafe actions such as reading `.env` secrets or claiming cloud deployment has happened.

## Problem

The course is short, dense, and operationally messy in the way real projects are messy. Each day has official discussion posts, whitepapers, podcasts, codelabs, livestreams, Discord context, local experiments, and human-only actions like claiming a badge or submitting a capstone. On top of that, optional cloud deployment introduces cost, credentials, IAM, and cleanup risk.

The core risk is not that a model cannot summarize. The risk is that a model can summarize too confidently from stale or incomplete context. For a capstone certificate path, that matters: daily assignments do not require output submission, but Kaggle's capstone project does require a submitted Writeup, video, and public project link. Mixing those two facts can mislead the user.

## Solution

Course Materials Ops Agent acts as an operations layer for the course workspace. It keeps a local source of truth and answers only from files that have been deliberately logged:

- `notes/course-log.md`
- `notes/link-log.md`
- `work/day-*/material-notes.md`
- `work/day-05/production-checklist.md`
- `capstone/*.md`
- `submissions/*.md`

The agent is implemented with ADK and Agents CLI. The LLM receives concise, source-labeled outputs from deterministic tools, while Python code enforces path allowlists and safety boundaries before any file content reaches the model.

## Architecture

The architecture is intentionally small:

```text
User prompt
  -> ADK Gemini agent
  -> deterministic local tools
  -> whitelisted course notes and submission files
  -> grounded answer
```

The agent has tools for:

- Listing readable course files.
- Reading a whitelisted file.
- Returning official links from the link log.
- Summarizing course status by day.
- Searching course notes.
- Checking cloud deployment readiness.
- Preparing a capstone summary.

This tool layer is the project boundary. The model can ask for information, but it cannot bypass the file allowlist or the deployment gate.

## Course Concepts Demonstrated

This submission demonstrates at least four concepts from the course:

1. **ADK / Agents CLI**: The agent is scaffolded and run with Agents CLI, and the core agent is defined with ADK.
2. **Agent skills and tool use**: The assistant calls deterministic tools for link lookup, status retrieval, file reads, search, and deployment readiness.
3. **Security features**: Secret files are blocked, secret-oriented searches are refused, and prompt-injection attempts are covered by tests/evals.
4. **Deployability**: The project includes FastAPI/Docker scaffolding and an explicit readiness gate for cloud deployment. It is not deployed by default because no billing project, dry run, or explicit deployment approval has been recorded.

Antigravity and MCP are intentionally not required for the current version. The project is designed so an MCP layer could be added later to expose the course workspace as a local resource server.

## Safety And Reliability

The agent has several guardrails:

- `.env` and `.kaggle` paths are blocked.
- Search requests containing `.env` or `secret` are refused.
- Cloud deployment is always refused unless the environment has `gcloud`, `GOOGLE_CLOUD_PROJECT`, credentials, dry-run review, and explicit user approval.
- The agent is instructed not to claim deployment, cleanup, CI/CD, billing, or publishing unless local notes prove it.

This matters because the course includes optional cloud codelabs. The agent should help the user understand those tasks without accidentally running or implying cost-incurring actions.

## Verification

The current project state has been verified locally:

- `uv run pytest`: 7 passed, 4 integration tests skipped by default.
- `agents-cli lint`: ruff, format, codespell, and ty passed.
- Live run: `agents-cli run "What is left for Day 5?"` completed successfully.
- Live safety run: `agents-cli run "Can we deploy the capstone to Google Cloud now?"` called the readiness tool and refused deployment.

An eval dataset is included at `tests/eval/datasets/basic-dataset.json`. It covers status, official links, deployment refusal, capstone summary generation, and a prompt-injection attempt asking for `.env`.

Managed eval trace generation is prepared but currently optional because it requires Google Cloud Application Default Credentials. Kaggle judging does not require a live deployed endpoint, so this submission uses a public code repository path instead.

## What I Learned

This project made the course's production message concrete: a useful agent is not only a prompt. The durable parts are the spec, trusted source files, deterministic tools, tests, safety rules, and honest operational status.

The biggest lesson was the distinction between prototype confidence and submission correctness. The agent originally helped track daily work, but after checking Kaggle's capstone requirements, the workspace had to distinguish "daily assignment outputs are not required" from "capstone participation is required for the Kaggle certificate path." That correction is now captured in the local notes and submission status.

## Limitations And Future Work

The current project is local-first. It does not include a public hosted demo, because the safer submission path is a public repository with setup instructions. Future work could add:

- A small read-only web UI.
- MCP resource exposure for the course workspace.
- Managed eval traces after Google Cloud ADC is configured.
- Agent Runtime or Cloud Run deployment after dry-run review and explicit approval.

## Project Link

https://github.com/hlgendr/course-materials-ops-agent

## Video

To be attached after recording a 5-minute-or-less YouTube demo.
