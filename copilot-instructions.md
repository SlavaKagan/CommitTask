# GitHub Copilot Instructions — Task Manager Demo Project

## Project Overview
This is a Python-based **Task Manager** module used as a training demo for GitHub Copilot
onboarding sessions at the bank's R&D organization.

## Language & Style
- **Language**: Python 3.11+
- **Type hints**: Always use full type hints on all function signatures
- **Docstrings**: Google-style docstrings on every public function
- **Naming**: `snake_case` for functions and variables, `UPPER_SNAKE_CASE` for constants

## Code Conventions
- Functions must be **pure where possible** — avoid hidden side effects
- Raise **specific exceptions** (`ValueError`, `KeyError`, `RuntimeError`) with descriptive messages
- Always wrap external I/O or risky operations in **try/except** blocks
- Keep functions **short** (under 30 lines); extract helpers if needed

## Testing
- Test framework: **pytest**
- Every function must have at least one **happy-path** and one **edge-case** test
- Use `@pytest.fixture(autouse=True)` to reset in-memory state between tests
- Test class names: `TestFunctionName`, test method names: `test_<what_it_does>`

## Domain Rules
- Valid priorities: `"low"`, `"medium"`, `"high"` — always validate
- Dates are stored as ISO 8601 strings (`YYYY-MM-DD`)
- Tasks are identified by integer `id` — never expose mutable internal IDs
- A completed task should **never** be modified after completion

## Comments & Documentation
- Add a module-level docstring to every file
- Inline comments only for **non-obvious** logic
- Copilot: when generating new functions, follow the existing patterns in `task_manager.py`

## What to Avoid
- No external dependencies beyond Python stdlib and pytest
- No database or file I/O in the core module (demo is in-memory only)
- No `print()` statements in production code (use logging if needed)
