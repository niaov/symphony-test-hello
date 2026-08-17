# symphony-test-hello

Minimal Python project for [Symphony](https://github.com/openai/symphony) verification testing.

## What's here

- `hello.py` — basic `add(a, b)` function
- `test_hello.py` — pytest tests
- `.github/workflows/ci.yml` — GitHub Actions CI (runs pytest on push + PR)

## How Symphony uses this repo

When Symphony picks up a GitHub issue from this repo, it:
1. Clones this repo into a per-issue workspace
2. Spawns a Codex agent to implement the issue
3. Codex commits, pushes a branch, creates a PR
4. CI runs `pytest`
5. When green + Symphony accepts, the PR lands

## Run locally

```bash
pip install pytest
pytest -v
python hello.py
```
