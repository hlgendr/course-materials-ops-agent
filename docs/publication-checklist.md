# Publication Checklist

Use this before creating a public repository link for Kaggle.

## Required For Kaggle

- [ ] Public project link is available.
- [ ] README explains the problem, solution, architecture, setup, and demo.
- [ ] Code repository has setup instructions.
- [ ] No credentials or private local state are included.
- [ ] The submission demonstrates at least three course concepts.

## This Project Covers

- [x] ADK / Agents CLI implementation.
- [x] Deterministic agent tools.
- [x] Security features for secrets and prompt injection.
- [x] Deployability via FastAPI/Docker scaffolding and readiness checks.
- [x] Evaluation dataset and unit tests.
- [ ] Public repository URL.
- [ ] Kaggle Writeup.
- [ ] Cover image.
- [ ] YouTube video.
- [ ] Kaggle submission.

## Pre-Publish Commands

Run from `capstone/course-ops-agent`:

```bash
uv run pytest
agents-cli lint
```

Run from the workspace root:

```bash
bash scripts/check_course_setup.sh
```

Run a public-files secret scan before pushing:

```bash
rg -n --hidden --glob '!.env' --glob '!**/.env' --glob '!**/.venv/**' \
  --glob '!**/.google-agents-cli/**' --glob '!**/.agents-cli-scripts/**' \
  --glob '!**/.adk/**' --glob '!**/__pycache__/**' \
  --glob '!capstone/course-ops-agent/docs/publication-checklist.md' \
  'AIza[0-9A-Za-z_-]{20,}|GOOGLE_API_KEY=AIza|GEMINI_API_KEY=AIza|BEGIN PRIVATE KEY|client_secret|refresh_token|password[[:space:]]*=' \
  capstone submissions notes work README.md docs scripts
```

Expected result: no real secret values. Placeholder strings in `.env.example`
are acceptable.

## User-Owned Actions

These should not be done automatically without confirmation:

- Join the Kaggle capstone competition and accept rules.
- Publish the code repository publicly.
- Choose final cover image style.
- Record and publish the YouTube video.
- Submit the Kaggle Writeup.
