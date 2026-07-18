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

## Feature Development Rules

- All forms must use `react-hook-form` with Zod validation. Validation logic must not be duplicated inside components.

- Every user-facing form field must include accessible labels and appropriate validation feedback using semantic HTML and ARIA attributes where required.

- A feature is not complete until its expected behavior is verified with tests covering validation, successful submission, and important edge cases.

- User input must be normalized before processing. Required text fields should handle whitespace-only values correctly.

- Async actions must provide clear user feedback, including loading states, disabled actions during submission, and error handling.

- New features should define requirements and expected behavior before implementation to reduce incorrect assumptions from AI-assisted development.

## Conventions
- Commit messages: Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, etc.)
- Keep functions small and single-purpose
- Prefer explicit error handling over silent failures
- No secrets or API keys committed — use `.env` (gitignored)

## Priorities
1. Correctness of the knowledge-base Q&A and escalation logic
2. Clean, demoable UI over premature scaling
3. Code should read clearly to a human reviewer, not just work