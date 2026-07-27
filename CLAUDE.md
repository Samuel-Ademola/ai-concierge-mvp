# CLAUDE.md

Guidance for Claude Code (and any AI assistant) working in this repository.

---

# Project

AI Concierge MVP is an AI-powered hospitality assistant for hotels, resorts, and short-term rentals.

The application helps guests communicate naturally with hospitality businesses by answering common questions, capturing guest preferences, collecting leads, and supporting human escalation when necessary.

The goal is to build a polished, production-style capstone project while following an AI-assisted software engineering workflow centered on planning, verification, testing, and documentation.

---

# Stack

## Backend

- Python
- FastAPI
- Pydantic
- Pytest

## Frontend

- React
- TypeScript
- Vite

## Development

- Git
- GitHub
- VS Code

---

# Repository Structure

```
app/
    routes/         API endpoints

    schemas/        Pydantic models

    services/       Business logic

frontend/
    React application

tests/
    Backend tests
```

---

# Conventions

- Use Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`).
- Keep functions small and focused on a single responsibility.
- Prefer explicit error handling over silent failures.
- Never commit secrets or API keys.
- Store configuration in `.env`.
- Write readable code that is easy for humans to review.

---

# Project Rules

## Forms

- Use controlled React components for all form inputs.
- Validate user input before submission.
- Reject empty or whitespace-only required values.
- Validate email addresses using explicit validation rules.
- Display clear validation messages to users.

## Architecture

- Keep UI components separate from business logic.
- Keep API routes lightweight.
- Place validation in schemas where appropriate.
- Keep business logic inside the services layer.

## AI Development Workflow

Every feature should follow this workflow:

1. Understand the requirements.
2. Create an implementation plan.
3. Generate code with clear constraints.
4. Review AI-generated code.
5. Run automated tests where available.
6. Perform manual verification.
7. Document important findings before merging.

AI-generated code is never accepted without verification.

## Testing

Before completing a feature:

- Verify the UI renders correctly.
- Test required validation.
- Test invalid input.
- Test edge cases.
- Confirm successful submission.
- Ensure imports and exports are correct.
- Verify the application builds successfully.

---

# Priorities

1. Correctness before speed.
2. Verification before acceptance.
3. Readability before cleverness.
4. Reliable guest experience.
5. Maintainable project structure.

---

# Coding Principles

- Prefer simple solutions over unnecessary complexity.
- Avoid duplicate logic.
- Use descriptive naming.
- Write components that are easy to test.
- Keep commits focused on a single change.

---

# AI Prompting Principles

When requesting implementation from an AI assistant:

- Provide project context.
- Reference the exact files involved.
- Specify constraints.
- Include expected behavior.
- Request verification steps.
- Ask for tests whenever practical.

Avoid vague implementation requests when building production features.

---

# Lessons Learned

The Guest Preferences workflow demonstrated that better prompts reduce review effort but do not eliminate the need for testing.

A real issue was discovered during UI verification when the expected implementation was missing from the active branch. The problem was identified through Git history inspection and corrected before final verification.

The primary value of AI-assisted development comes from structured planning, verification, and review—not simply generating code faster.