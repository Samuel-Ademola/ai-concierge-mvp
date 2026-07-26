# AI Development Workflow Comparison

## Feature

Guest Preferences Settings feature for AI Concierge MVP.

Stack:

Backend:
- Python
- FastAPI
- Pydantic
- Pytest

Frontend:
- React
- TypeScript
- Vite


# Round 1 — Vague Prompt

## Prompt Used

Create a guest preferences settings feature.

## Process

- Started from the main branch.
- Created a separate branch:
  `feature/react-form-vague`
- Used a fresh AI session.
- Provided minimal context.
- Accepted the generated implementation and reviewed afterward.

## Result

The AI generated:

- React form component
- State management
- Basic validation
- Input handling
- Submit behavior

## Review Notes

The implementation worked, but the AI made assumptions about:

- Field naming
- Validation requirements
- Error message behavior
- Data structure

More manual review was required because the requirements were not clearly defined.


# Round 2 — Specification-Driven Prompt

## Prompt Used

The AI was given:

- Project context
- File references
- Required fields
- Validation rules
- Expected behavior
- Component constraints
- Verification requirements

## Process

- Created branch:
  `feature/react-form-spec`
- Used a structured explore-plan-code approach.
- Required implementation plus verification.

## Result

The implementation included:

- Controlled React inputs
- TypeScript types
- Validation functions
- Error states
- Accessible labels
- Character limit handling
- Submit workflow

## Improvements Compared With Round 1

Specific differences:

| Area | Vague Prompt | Specification Prompt |
|---|---|---|
| Requirements | AI assumptions | Defined behavior |
| Validation | Basic assumptions | Explicit rules |
| Accessibility | Not guaranteed | Labels and form structure included |
| Review effort | Higher | Lower |
| Maintainability | Required more checking | Easier to verify |


# Verification Findings

During UI testing, the first implementation attempt exposed an issue.

The spec branch contained a placeholder version of:

`frontend/src/components/GuestPreferencesForm.tsx`

instead of the intended validated implementation.

The issue was discovered during browser testing when the UI only displayed:

- Guest Preferences Form
- Empty inputs
- Submit button

The problem was traced using Git history:

- `feature/react-form-vague` contained the complete implementation.
- The correct component was restored and verified.

This reinforced an important lesson:

AI-generated code is not complete until the current branch has been tested and verified.


# QA Verification

The Guest Preferences UI was tested for:

## Rendering

- Component loaded successfully
- React import/export verified
- UI displayed correctly

## Validation

Tested:

- Empty required fields
- Invalid email formats
- Whitespace input handling
- Required selections

## User Experience

Verified:

- Dropdown selections
- Character counter
- Submit behavior
- Error messages
- Accessibility labels


# AI Mistakes Caught

During development, the following issues were identified:

1. AI-generated component integration issue:
   - Incorrect import/export relationship caused the React page to fail.

2. Branch verification issue:
   - The expected implementation was not present in the current branch despite existing in Git history.

These issues were fixed through testing and repository inspection.


# Project Rules Learned

The following rules were added to CLAUDE.md:

1. Components should have clear exports and predictable import paths.

2. Every feature should include verification steps before acceptance.

3. AI-generated code must be reviewed against project requirements before merging.


# Final Workflow

The preferred AI development workflow for future features:


Requirement
↓
Specification
↓
AI implementation
↓
Code review
↓
Automated tests
↓
Manual verification
↓
Documentation
↓
Merge




# Lessons Learned

AI increases development speed, but reliability comes from:

- Clear requirements
- Verification loops
- Testing
- Git discipline
- Human review

The goal is not simply generating code faster.

The goal is building software that can be trusted.