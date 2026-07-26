# AI Development Workflow Comparison

## Feature

Guest Preferences Settings Feature for AI Concierge MVP

Stack:
- React + TypeScript
- Python + FastAPI
- Pydantic
- Pytest

## Objective

This experiment compares two AI-assisted development approaches for building the same feature.

The goal was to understand the difference between simply asking AI to generate code and using AI as an engineering assistant through specifications, planning, constraints, and verification.

---

# Round 1 — Vague Prompt Approach

## Prompt Used

"Create a guest preferences settings feature for my application."

The implementation was created in a fresh AI session using minimal context. The AI was allowed to make decisions about structure, validation, and testing.

## Result

The AI successfully generated a working feature including:

- Guest preferences data model
- API routes
- Validation schema
- Service logic
- Basic tests

However, because the requirements were not clearly defined, the AI made assumptions.

## Issues Found During Review

The generated implementation required additional review because:

- Validation requirements were incomplete.
- Some edge cases were not considered.
- Testing coverage depended on AI assumptions.
- Accessibility and user experience requirements were not specified.
- Some project structure decisions needed adjustment.

The code worked, but more developer time was required to verify and improve the output.

---

# Round 2 — Specification-Driven Approach

## Prompt Strategy

The second implementation used a detailed engineering specification.

The prompt included:

- Relevant project files
- Feature requirements
- Validation rules
- Expected user behaviour
- Architecture constraints
- Testing requirements
- Verification instructions

The AI was instructed to first create a plan, implement the feature, write tests, and verify the result.

## Result

The structured workflow produced a more reliable implementation.

Improvements included:

- Clear separation of concerns
- Stronger validation rules
- Better handling of invalid user input
- More complete automated tests
- Reduced manual refactoring

The development process initially took slightly longer because planning was required, but the total review and correction time was lower.

---

# Comparison

## Correctness

The specification-driven approach produced more predictable results because requirements were explicit. The AI had fewer opportunities to make assumptions.

## Accessibility

The structured workflow encouraged consideration of user experience requirements such as clear labels, meaningful validation messages, and keyboard-friendly interactions.

## Edge Cases

The second approach handled cases such as:

- Empty guest names
- Whitespace-only values
- Invalid email formats
- Requests exceeding maximum length
- Missing required fields

## Review Effort

The vague prompt approach required more debugging and manual inspection.

The specification approach shifted the developer role from fixing generated code to reviewing engineering decisions and verifying correctness.

---

# AI Mistake Discovered

During review, an AI-generated implementation allowed whitespace-only names because it only checked whether the field existed.

This was identified through validation testing and corrected by adding explicit input validation.

---

# Lessons Added to CLAUDE.md

Based on this experiment, project rules were added:

1. Forms must include validation before submission.
2. New features require automated tests.
3. UI components and business logic should remain separated.

---

# Conclusion

This experiment showed that effective AI-assisted development depends on engineering discipline.

AI can generate code quickly, but reliable software requires clear specifications, verification loops, testing, and human review.

The developer's role is not replaced by AI; it becomes more focused on architecture, requirements, and quality control.