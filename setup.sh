#!/bin/bash
set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Job Hunter Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check for required tools
echo ""
echo "Checking prerequisites..."

if ! command -v uvx &> /dev/null; then
  echo "  [!] uvx not found. Installing uv..."
  pip install uv
  echo "  [✓] uv installed"
else
  echo "  [✓] uvx found: $(uvx --version 2>/dev/null || echo 'ok')"
fi

if ! command -v npx &> /dev/null; then
  echo "  [✗] npx not found. Please install Node.js from https://nodejs.org"
  echo "      Node.js is required for Playwright MCP and filesystem MCP."
  exit 1
else
  echo "  [✓] npx found: $(node --version)"
fi

if ! command -v sqlite3 &> /dev/null; then
  echo "  [!] sqlite3 CLI not found. Attempting install..."
  if command -v brew &> /dev/null; then
    brew install sqlite
  elif command -v apt-get &> /dev/null; then
    sudo apt-get install -y sqlite3
  else
    echo "  [!] Could not install sqlite3 automatically. Please install it manually."
    echo "      macOS: brew install sqlite"
    echo "      Ubuntu: sudo apt-get install sqlite3"
  fi
else
  echo "  [✓] sqlite3 found: $(sqlite3 --version)"
fi

# Create directory structure
echo ""
echo "Creating directories..."
mkdir -p data
mkdir -p output/resumes
mkdir -p output/covers
echo "  [✓] data/"
echo "  [✓] output/resumes/"
echo "  [✓] output/covers/"

# Initialize SQLite database
echo ""
echo "Initializing database..."
if [ -f "./data/schema.sql" ]; then
  sqlite3 ./data/jobs.db < ./data/schema.sql
  echo "  [✓] Database initialized at ./data/jobs.db"
else
  echo "  [✗] schema.sql not found at ./data/schema.sql"
  exit 1
fi

# Verify MCP config
echo ""
echo "Verifying MCP configuration..."
if [ -f "./.mcp.json" ]; then
  echo "  [✓] .mcp.json found"
else
  echo "  [✗] .mcp.json not found — MCP servers will not be available"
fi

# Pre-fetch MCP servers (optional, speeds up first run)
echo ""
echo "Pre-fetching MCP servers (this may take a moment)..."
echo "  Checking jobspy-mcp-server..."
uvx jobspy-mcp-server --help &> /dev/null && echo "  [✓] jobspy-mcp-server available" || echo "  [!] jobspy-mcp-server will be fetched on first use"

echo "  Checking mcp-server-sqlite..."
uvx mcp-server-sqlite --help &> /dev/null && echo "  [✓] mcp-server-sqlite available" || echo "  [!] mcp-server-sqlite will be fetched on first use"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Setup complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "  1. Run:  claude"
echo "  2. Then: /job-hunter:discover"
echo "  3. Then: /job-hunter:review"
echo "  4. Then: /job-hunter:apply [id]"
echo ""
echo "Daily workflow:"
echo "  Morning  → /job-hunter:discover"
echo "  Morning  → /job-hunter:review"
echo "  Midday   → /job-hunter:apply (up to 8/day)"
echo "  Anytime  → /job-hunter:watchlist"
echo "  Weekly   → /job-hunter:follow-up"
echo "  Anytime  → /job-hunter:status"
echo ""
