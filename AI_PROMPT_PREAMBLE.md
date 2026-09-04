# AI Engineering Prompt Preamble

You are assisting with development of the AI Concierge MVP.

Before writing code:

1. Understand the existing project architecture.
2. Review relevant files before proposing changes.
3. Explain the implementation plan before coding.

Engineering rules:

## Architecture

- Keep API routes, schemas, services, and UI components separated.
- Do not place business logic directly inside UI components.
- Follow existing project structure before creating new files.

## Forms and Validation

- All forms must include validation.
- Reject invalid or incomplete user input.
- Provide clear user-facing error messages.
- Consider accessibility requirements.

## Testing

- New features require automated tests.
- Verify expected behaviour and edge cases.
- Do not consider a feature complete without validation.

## Verification Loop

After implementation:

1. Explain what changed.
2. Run relevant tests.
3. Report failures.
4. Suggest improvements if issues remain.

Code quality expectations:

- Prefer maintainable solutions over quick hacks.
- Follow existing naming conventions.
- Avoid unnecessary dependencies.