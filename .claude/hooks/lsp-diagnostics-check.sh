#!/bin/bash
#
# PostToolUse Hook: LSP Diagnostics Check
#
# Queries the LSP bridge daemon for TypeScript/Python diagnostics after a
# file is written or edited. Returns errors/warnings as additionalContext
# so Claude sees them immediately.
#
# Input (stdin): JSON with tool_input.file_path
# Output (stdout): JSON with hookSpecificOutput.additionalContext (if errors)

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
SOCKET_FILE="$PROJECT_DIR/.claude/hooks/lsp-bridge.socket"

# Read the hook input from stdin
INPUT=$(cat)

# Extract the file path
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [ -z "$FILE_PATH" ]; then
  echo '{}'
  exit 0
fi

# Only check supported file types (TypeScript/JavaScript/Python)
case "$FILE_PATH" in
  *.ts|*.tsx|*.js|*.jsx|*.py|*.pyi) ;;
  *)
    echo '{}'
    exit 0
    ;;
esac

# Check if the LSP bridge is running
if [ ! -f "$SOCKET_FILE" ]; then
  # Bridge not running — skip silently
  echo '{}'
  exit 0
fi

SOCKET_PATH=$(cat "$SOCKET_FILE")

if [ ! -S "$SOCKET_PATH" ]; then
  # Socket doesn't exist — bridge probably died
  echo '{}'
  exit 0
fi

# Query the bridge for diagnostics
RESPONSE=$(curl -s --unix-socket "$SOCKET_PATH" \
  -X POST \
  -H "Content-Type: application/json" \
  -d "{\"file\": \"$FILE_PATH\"}" \
  "http://localhost/diagnostics" 2>/dev/null) || {
  # curl failed — bridge may be down
  echo '{}'
  exit 0
}

# Check if we got a valid response with diagnostics
DIAG_COUNT=$(echo "$RESPONSE" | jq '.diagnostics | length' 2>/dev/null) || {
  echo '{}'
  exit 0
}

if [ "$DIAG_COUNT" -eq 0 ]; then
  echo '{}'
  exit 0
fi

# Format diagnostics into a readable string for Claude
CONTEXT=$(echo "$RESPONSE" | jq -r '
  .diagnostics[] |
  "\(.severity | ascii_upcase): \(.message) (line \(.range.start.line), col \(.range.start.character))" +
  (if .code then " [\(.source) \(.code | tostring)]" else "" end)
')

# Build the hook response with additionalContext
jq -n --arg ctx "LSP Diagnostics for $FILE_PATH:
$CONTEXT" '{
  hookSpecificOutput: {
    hookEventName: "PostToolUse",
    additionalContext: $ctx
  }
}'
