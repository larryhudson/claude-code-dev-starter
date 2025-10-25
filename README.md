# Claude Code Dev Starter Template

A production-ready template for setting up new projects optimized for working with [Claude Code](https://docs.claude.com/en/docs/claude-code/). This template includes development tools, linting hooks, CI/CD pipelines, and Claude Code integrations to streamline your development workflow.

## What's Included

### Development Setup

- **Makefile**: Convenient commands for managing your development environment
  - `make dev`: Start your development server using hivemind with process management
  - `make dev-logs`: View and tail development logs (with ANSI codes stripped for readability)
  - `make lint`: Lint Python files with ruff
  - `make format`: Format Python files with ruff
  - `make type-check`: Type check with ty
  - `make lint-file FILE=path/to/file`: Lint and format a specific file
  - `make stop-dev`: Stop the running development server

- **Procfile**: Configuration file for hivemind to manage multiple development processes
  - FastAPI development server with auto-reload
  - Can be extended with additional processes

### Claude Code Integration

- **Hook Configuration** (`.claude/settings.json`): Registers hooks with Claude Code
  - PostToolUse hook runs on Write/Edit tools with 30-second timeout
  - SessionStart hook runs on session initialization with 60-second timeout

- **PostToolUse Hook** (`.claude/hooks/post-tool-use.py`): Python script that automatically runs checks after Claude modifies files
  - Reads configuration from `.post-claude-edit-config.yaml`
  - Matches modified files against glob patterns
  - Runs configured commands with proper substitution (`{file}`, `{dir}`)
  - Returns structured JSON feedback to Claude Code
  - Ensures code style consistency without manual intervention

- **Post-Claude-Edit Configuration** (`.post-claude-edit-config.yaml`): Defines what checks run after edits
  - Pattern-based file matching (e.g., `*.ts`, `*.tsx`)
  - Flexible command configuration
  - Enable/disable checks without removing them
  - Includes helpful examples

- **SessionStart Hook** (`.claude/hooks/session-start.sh`): Runs when a Claude Code session starts
  - Checks for required development tools (hivemind, jq, npm)
  - Installs npm dependencies if needed
  - Provides helpful context about available commands

### Code Quality

- **.pre-commit-config.yaml**: Pre-commit hooks for automated code quality checks
  - Trailing whitespace removal
  - End-of-file fixing
  - YAML validation
  - Large file detection
  - JSON validation
  - Merge conflict detection
  - Optional: ESLint configuration (commented out for flexibility)

### CI/CD

- **.github/workflows/ci.yaml**: GitHub Actions workflow for automated testing and linting
  - Runs on push to main/develop branches and pull requests
  - Lint job: Checks code style and formatting
  - Test job: Runs your test suite
  - Node.js 18 environment with npm caching

## Getting Started

### 1. Installation

```bash
# Install hivemind (for process management)
# On macOS
brew install hivemind

# On Linux
# Follow instructions at https://github.com/DarthSim/hivemind

# Install pre-commit framework
pip install pre-commit

# Set up pre-commit hooks
pre-commit install

# Install Python dependencies for Claude Code hooks
pip install pyyaml
```

### 2. Configure Your Project

1. Update `Procfile` with your project's development commands:
   ```
   web: npm run dev
   ts-watch: npm run ts:watch
   tests: npm run test:watch
   ```

2. Update `.post-claude-edit-config.yaml` with checks you want to run:
   ```yaml
   checks:
     - name: lint-typescript
       patterns: ['*.ts', '*.tsx', '*.js', '*.jsx']
       command: 'npm run lint -- --fix {file}'
       enabled: true
   ```
   - Uncomment examples to enable them
   - Add custom checks for your project
   - Use `{file}` placeholder for the modified file path
   - Set `enabled: false` to disable checks temporarily

3. Update `.pre-commit-config.yaml` with hooks relevant to your project:
   - Uncomment the ESLint section if using JavaScript/TypeScript
   - Add additional hooks for your language/framework

4. Update `.github/workflows/ci.yaml` with your actual npm scripts:
   - Ensure `npm run lint`, `npm run format:check`, and `npm test` exist
   - Or adjust the commands to match your project

### 3. Claude Code Configuration

The Claude Code hooks are already configured in `.claude/settings.json`. The configuration includes:

- **PostToolUse Hook**: Automatically runs checks after Write/Edit tools
  - Triggered when Claude modifies files
  - Runs matching checks from `.post-claude-edit-config.yaml`
  - 30-second timeout per command

- **SessionStart Hook**: Prepares development environment
  - Checks for required tools
  - Installs dependencies
  - Provides context about available commands
  - 60-second timeout

No additional configuration needed—the hooks will run automatically in Claude Code!

## Usage Examples

### Starting Development

```bash
# Start all processes defined in Procfile
make dev

# In another terminal, view live logs
make dev-logs

# When done, stop the server
make stop-dev
```

### Working with Claude Code

1. **Edit a file**: Claude modifies `src/app.ts`
2. **Automatic formatting**: The PostToolUse hook runs `make lint-file FILE=src/app.ts`
3. **Result**: File is automatically linted and formatted

### Manual Linting

```bash
# Lint and format a specific file
make lint-file FILE=src/utils/helpers.ts

# Or use your linter directly
npm run lint -- --fix src/utils/helpers.ts
```

### Running Pre-commit Checks

```bash
# Run all pre-commit checks on staged files
pre-commit run

# Run all pre-commit checks on all files
pre-commit run --all-files

# Update hook versions
pre-commit autoupdate
```

## File Structure

```
.
├── .claude/
│   ├── settings.json              # Claude Code hook configuration
│   └── hooks/
│       ├── post-tool-use.py       # Python script for post-edit checks
│       └── session-start.sh        # Bash script for session setup
├── .github/
│   └── workflows/
│       └── ci.yaml                # GitHub Actions CI/CD pipeline
├── .post-claude-edit-config.yaml   # Post-edit checks configuration
├── .pre-commit-config.yaml         # Pre-commit hook configuration
├── Makefile                        # Development commands
├── Procfile                        # Process definitions for hivemind
└── README.md                       # This file
```

## Customization

### Adding Post-Claude-Edit Checks

Edit `.post-claude-edit-config.yaml` to add or modify checks:

```yaml
checks:
  - name: format-json
    patterns: ['*.json']
    command: 'npx prettier --write {file}'
    enabled: true

  - name: typecheck
    patterns: ['*.ts', '*.tsx']
    command: 'npm run type-check'
    enabled: true

  - name: test-file
    patterns: ['src/**/*.ts']
    command: 'npm test -- {file}'
    enabled: false  # Disabled for now
```

- **patterns**: Glob patterns to match file paths (fnmatch style)
- **command**: Command to execute (use `{file}` for file path, `{dir}` for directory)
- **enabled**: Toggle without deleting the check

### Adding More Make Targets

Edit `Makefile` to add custom targets:

```makefile
build:
	npm run build

deploy:
	npm run deploy
```

### Adding More Processes

Edit `Procfile` to add or remove processes:

```procfile
web: npm run dev
api: npm run api
db: docker-compose up
```

### Extending Pre-commit Hooks

Uncomment or add hooks to `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/your-org/custom-hooks
  rev: v1.0.0
  hooks:
    - id: custom-check
```

### Customizing Hook Timeouts

Edit `.claude/settings.json` to adjust hook timeouts:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/post-tool-use.py",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

Increase timeout if your checks take longer to run.

## Troubleshooting

### Dev server already running

If you see "Dev server is already running", you can either:
- Run `make stop-dev` to stop the existing server
- Check the `.dev.pid` file to see the PID

### Hooks not executing

Ensure hooks are executable:
```bash
chmod +x .claude/hooks/*.sh
```

### Pre-commit issues

Update pre-commit and hooks:
```bash
pre-commit clean
pre-commit autoupdate
pre-commit run --all-files
```

## Learn More

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/)
- [Hivemind Documentation](https://github.com/DarthSim/hivemind)
- [Pre-commit Framework](https://pre-commit.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## License

This template is provided as-is for use with Claude Code projects.
