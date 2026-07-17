# CLAUDE.md

Guidance for Claude Code (and any AI assistant) working in this repo.

## Project
AI concierge MVP for hospitality businesses. Guests chat with an assistant
that answers from a business knowledge base, captures leads, and escalates
to a human when it can't help. Goal: a polished, pilot-worthy demo — not a
toy built around a fake property.

## Stack
Not finalized yet. Update this section once chosen — note the language,
framework, and any key libraries so future assistant sessions don't guess.

## Conventions
- Commit messages: Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, etc.)
- Keep functions small and single-purpose
- Prefer explicit error handling over silent failures
- No secrets or API keys committed — use `.env` (gitignored)

## Priorities
1. Correctness of the knowledge-base Q&A and escalation logic
2. Clean, demoable UI over premature scaling
3. Code should read clearly to a human reviewer, not just work