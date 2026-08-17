# AGENTS.md - Symphony test repo

## Repository purpose

Minimal Python project for verifying the [Symphony](https://github.com/openai/symphony)
orchestration system. Issues filed here should be small, self-contained coding
tasks (add a function, fix a typo, add a test case) suitable for autonomous
agent completion in 1-3 turns.

## Layout

- `hello.py` — module under test
- `test_hello.py` — pytest tests
- `.github/workflows/ci.yml` — CI: pytest on push + PR

## Conventions

- Functions live in `hello.py`, tests mirror them in `test_hello.py`.
- Use type hints.
- Run `pytest -v` before considering work done.
- Commit message format: `<type>: <subject>` (e.g. `feat: add multiply function`).

## CI

CI runs `pytest -v` on every push and PR. Work is not complete until CI is green.
