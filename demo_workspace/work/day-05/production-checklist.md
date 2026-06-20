# Day 5 Production Checklist

Use this checklist before turning the prototype into a deployed agent.

## Must Have Locally

- [x] Agent purpose is written as a spec.
- [x] Out-of-scope requests have explicit behavior.
- [x] Deterministic rules run before LLM answers where possible.
- [x] Secrets are excluded from notes and repository files.
- [x] Prompt-injection and secret-handling cases exist in the eval dataset.
- [x] Code tests cover utility functions.
- [x] A cleanup plan is required before cloud resources are created.

## Cloud Deployment Gate

Do not deploy until all of these are true:

- [ ] User confirms a billing-enabled Google Cloud project.
- [ ] User confirms the target project ID.
- [ ] `gcloud` is installed and authenticated.
- [ ] Required APIs are enabled intentionally.
- [ ] User approves the deployment target.
- [ ] `agents-cli deploy --dry-run` output is reviewed.
- [ ] User explicitly approves any real deployment command.

## Current Demo Policy

Cloud deployment is intentionally blocked. A public code repository is sufficient
for Kaggle capstone submission when a live public demo is not feasible.
