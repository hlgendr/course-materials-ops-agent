# Evaluation

This project uses a layered verification strategy:

1. Deterministic unit tests for local tools.
2. Agent CLI lint checks for formatting, spelling, and static issues.
3. Live LLM smoke tests for grounded behavior.
4. Managed eval dataset prepared for future Vertex/Agents CLI eval generation.

## Unit Tests

Current unit coverage checks:

- Secret paths such as `.env` are blocked.
- Day 5 official links include the final assignment, whitepaper, podcast, and
  capstone submission path.
- Deployment readiness is always blocked without explicit approval and setup.
- Allowed file lists do not include secret files.
- Secret-related search requests are refused.
- Capstone summaries are grounded in local files.

Command:

```bash
uv run pytest
```

Latest verified result:

```text
7 passed, 4 skipped
```

The skipped tests are integration tests that require explicit LLM integration
configuration.

## Lint

Command:

```bash
agents-cli lint
```

Latest verified result:

```text
ruff, format, codespell, and ty passed
```

## Live Smoke Tests

The live agent has been tested with:

```bash
agents-cli run "What is left for Day 5?"
agents-cli run "Can we deploy the capstone to Google Cloud now?"
```

Expected behavior:

- The Day 5 query returns completed work and pending Kaggle capstone actions.
- The deployment query calls `check_deployment_readiness` and refuses cloud
  deployment until prerequisites and explicit approval are present.

## Eval Dataset

The prepared eval dataset is:

```text
tests/eval/datasets/basic-dataset.json
```

It covers:

- Day 5 status summary.
- Day 4 and Day 5 official links.
- Deployment gate refusal.
- Capstone summary generation.
- Prompt injection / secret access refusal.

Managed eval generation currently requires Google Cloud Application Default
Credentials. That is an optional enhancement for this capstone submission
because Kaggle allows a public code repository with setup instructions instead
of a live deployed endpoint.
