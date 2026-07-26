# CLAUDE.md

Guidance for Claude Code (and any AI assistant) working in this repo.

## Project

AI Concierge MVP is an AI-powered hospitality assistant for hotels,
resorts, and short-term rentals.

The system helps guests communicate with hospitality businesses by answering
questions, capturing preferences, supporting requests, and providing a
foundation for escalation to human staff.

The goal is a polished, pilot-ready hospitality product — not a toy demo.

---

## Stack

### Backend

- Python
- FastAPI
- Pydantic
- Pytest

### Frontend

- React
- TypeScript
- Vite

### Development Tools

- Git
- GitHub
- VS Code
- Claude Code

---

## Architecture Rules

- Keep API routes, schemas, services, and UI components separated.
- Business logic should not be placed directly inside UI components.
- Follow the existing project structure before creating new files.
- Reuse existing utilities and patterns before introducing new dependencies.

---

## Form Rules

- All forms must include validation.
- Reject empty or invalid user input.
- Prevent whitespace-only values.
- Provide clear user-facing validation messages.
- Consider accessibility when creating user interfaces.

---

## Testing Rules

- New features must include appropriate tests.
- AI-generated code must be reviewed before acceptance.
- Verify edge cases, not only the happy path.
- A feature is not complete until it has been tested.

---

## AI Development Workflow

When implementing a new feature:

1. Understand the requirement.
2. Review relevant files before coding.
3. Create an implementation plan.
4. Implement the solution.
5. Write or update tests.
6. Run verification.
7. Review the result for bugs and edge cases.

Do not generate code without understanding the existing architecture.

---

## Conventions

- Commit messages follow Conventional Commits:
  - `feat:`
  - `fix:`
  - `chore:`
  - `docs:`

- Keep functions small and single-purpose.
- Prefer explicit error handling over silent failures.
- Use clear naming conventions.
- No secrets or API keys committed.
- Use `.env` files for local configuration.

---

## Priorities

1. Correctness and reliability
2. Clear, maintainable code
3. Good guest experience
4. Clean demo-ready UI
5. Avoid premature complexity

Code should be understandable to a human reviewer, not only functional.