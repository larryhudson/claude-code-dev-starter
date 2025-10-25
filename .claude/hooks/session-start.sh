#!/bin/bash

# SessionStart Hook for Claude Code
# This hook runs when a Claude Code session starts
# It ensures dev dependencies are set up and provides development context

cd "$CLAUDE_PROJECT_DIR" || exit 1

# Check if required tools are installed
MISSING_TOOLS=()

if ! command -v hivemind &> /dev/null; then
  MISSING_TOOLS+=("hivemind")
fi

if ! command -v jq &> /dev/null; then
  MISSING_TOOLS+=("jq")
fi

if ! command -v npm &> /dev/null; then
  MISSING_TOOLS+=("npm")
fi

# Report missing tools
if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
  echo "Warning: The following development tools are not installed:"
  printf '  - %s\n' "${MISSING_TOOLS[@]}"
  echo ""
  echo "Please install them to use the full development setup."
fi

# Ensure npm dependencies are installed if package.json exists
if [ -f "package.json" ] && [ ! -d "node_modules" ]; then
  echo "Installing npm dependencies..."
  npm install
fi

# Provide development context
echo "Development environment loaded for: $CLAUDE_PROJECT_DIR"
echo "Available commands:"
echo "  - make dev       : Start development server"
echo "  - make dev-logs  : View development logs"
echo "  - make lint-file : Lint and format a specific file"
