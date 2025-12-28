# Claude Code Guidelines

## Environment Setup

### Pre-commit hooks
- **NEVER skip pre-commit hooks** with `--no-verify`
- If pre-commit fails, fix the environment instead of bypassing it
- Ensure `pre-commit` is in the dev dependencies in `pyproject.toml`
- Run `uv sync` to install dev dependencies including pre-commit
- Use `uv run pre-commit` or activate the venv to run pre-commit

### Running commands with uv
- Use `uv run <command>` to run Python tools (e.g., `uv run ruff check .`)
- Or prefix commands with the venv Python: `.venv/bin/python`
- The PATH may not include uv by default - use `$HOME/.local/bin/uv` if needed

## Package Management

- Use **npm** (not pnpm) for frontend packages
- Use **uv** for Python package management
- Add dev dependencies to `[dependency-groups] dev` in pyproject.toml
