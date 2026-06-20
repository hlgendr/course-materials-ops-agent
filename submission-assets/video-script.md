# Capstone Video Script

Target length: 4:30 to 5:00.

Working title: Course Materials Ops Agent - grounded course operations with safety gates.

## Recording Plan

Record a screen walkthrough with voiceover. The video does not need cloud
deployment. It should show the local project, one or two live commands, and the
Kaggle submission logic.

## Timeline

### 0:00-0:25 - Hook

Say:

"This is Course Materials Ops Agent, a local-first assistant I built for the
Kaggle 5-Day AI Agents course. The problem is not just summarizing notes. The
problem is keeping a fast-moving course workspace honest: what is official,
what is done, what still needs human action, and what should not be deployed
yet."

Show:

- Project README title.
- `submissions/final-assignment-status.md`.

### 0:25-1:05 - Problem And Value

Say:

"During the course, daily assignments, codelabs, podcasts, badge links, and
capstone requirements can easily get mixed together. The most important example
is that daily assignment outputs do not need to be submitted, but the Kaggle
certificate path still requires participation in the capstone project. This
agent keeps those distinctions grounded in local notes."

Show:

- `work/day-05/material-notes.md`
- `submissions/final-assignment-status.md`

### 1:05-1:55 - Architecture

Say:

"The architecture is deliberately small. An ADK Gemini agent calls deterministic
Python tools. The tools read only whitelisted files like the course log, link
log, material notes, and submission status. The LLM decides which tool to call,
but ordinary code enforces the safety boundary before content reaches the
model."

Show:

- `docs/architecture.md`
- `app/agent.py`
- `app/course_tools.py`

### 1:55-2:45 - Live Demo: Grounded Status

Run:

```bash
agents-cli run "What is left for Day 5?"
```

Say:

"Here the agent should answer from local course status and link logs. It should
separate completed local work from pending Kaggle capstone submission actions."

Show:

- Tool calls if visible.
- Final answer summary.

### 2:45-3:35 - Live Demo: Safety Gate

Run:

```bash
agents-cli run "Can we deploy the capstone to Google Cloud now?"
```

Say:

"This is the safety behavior I wanted. The agent does not say yes just because
the code exists. It calls a readiness tool and refuses deployment because
gcloud, project configuration, ADC, dry-run review, and explicit user approval
are not present."

Show:

- `check_deployment_readiness` output or final refusal.
- `work/day-05/production-checklist.md`.

### 3:35-4:20 - Verification

Run or show cached terminal:

```bash
uv run pytest
agents-cli lint
```

Say:

"The deterministic tools are covered by unit tests. The project also includes
an eval dataset for status, official links, deployment refusal, capstone
summary, and prompt-injection resistance."

Show:

- `docs/evaluation.md`
- `tests/eval/datasets/basic-dataset.json`

### 4:20-4:50 - Course Concepts And Close

Say:

"This capstone demonstrates ADK and Agents CLI, deterministic tool use, safety
features for secrets and deployment, and deployability through FastAPI and
Docker scaffolding. The result is a small but practical agent that turns course
chaos into auditable operational status."

Show:

- README "Kaggle Submission Fit" section.
- Public repo link page if available.

## Notes Before Recording

- Do not show `.env`.
- Do not show API keys, tokens, local account secrets, or browser password
  managers.
- Keep terminal font large.
- Close unrelated browser tabs and notifications.
- Use the final public repository link in the ending slide once it exists.
