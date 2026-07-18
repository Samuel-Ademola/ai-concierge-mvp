# AI Workflow Comparison — Settings Form Implementation

## Feature

Settings Form / Guest Preferences Settings Form

This feature was implemented twice using two different AI-assisted development workflows.

---

# Round 1 — Vague Prompt Workflow

Branch:

`feature/settings-vague`

Prompt:

"Build a settings form with validation in React."

The first implementation was generated with minimal context and requirements. The AI created a functional form structure, but important engineering decisions were left open.

## Findings

### Correctness

The implementation included basic validation for required fields and email formatting. However, validation logic was placed closer to the component instead of being separated into a reusable schema.

The AI also introduced additional assumptions such as numeric settings and time-related validation that were not part of the actual Guest Preferences requirements.

### Accessibility

The form included labels and used native HTML controls, which provided a good foundation. However, additional accessibility improvements were missing, including:

- `aria-invalid` for invalid fields
- `aria-describedby` connections between fields and errors
- improved screen reader error announcements

### Edge Cases

The implementation identified possible issues such as:

- empty submissions
- invalid emails
- duplicate submissions
- network failures

However, these were mostly recommendations rather than implemented protections.

---

# Round 2 — Specification-Driven Workflow

Branch:

`feature/settings-spec`

The second implementation used a detailed prompt containing:

- React Hook Form requirement
- Zod validation requirement
- TypeScript requirement
- Accessibility requirements
- Testing requirements
- Verification steps

## Improvements

### Correctness

Validation was moved into a dedicated Zod schema, creating a single source of truth.

The form uses:

- react-hook-form
- @hookform/resolvers/zod
- z.infer for TypeScript types

This reduced duplicated validation logic and improved maintainability.

### Accessibility

The improved version added:

- linked labels using `htmlFor` and `id`
- `aria-invalid`
- `aria-describedby`
- `role="alert"` error messages

Keyboard navigation was also verified.

### Testing

The second workflow added automated coverage for:

- required field validation
- invalid email handling
- successful submission
- submission state behaviour

---

# Specific Differences Between Branches

1. Round 1 used component-level validation, while Round 2 used a dedicated Zod schema.

2. Round 1 had accessibility recommendations, while Round 2 implemented ARIA error states.

3. Round 1 suggested testing, while Round 2 included actual form behavior tests.

4. Round 2 reduced review effort because requirements were defined before implementation.

---

# AI Mistake Identified

One AI mistake discovered during review was that the first generated implementation introduced validation requirements that were not part of the requested feature, including unrelated numeric and time-based settings.

The AI also did not initially handle whitespace-only text input correctly. This required additional validation thinking and demonstrated why generated code must be reviewed.

---

# Rules Added to CLAUDE.md

The following project rules were created from this exercise:

- Forms must use react-hook-form with Zod validation.
- Validation rules must be separated from UI components.
- Every input requires an accessible label.
- Features are not complete until tests verify expected behaviour.
- Async submissions must handle loading and failure states.

---

# Review Effort

The first implementation required more investigation because requirements were unclear and missing pieces had to be identified manually.

The second implementation required more planning upfront but reduced debugging and review time because the expected behaviour was already defined.

This exercise showed that effective AI-assisted development depends on clear specifications, verification, and review rather than simply generating code.