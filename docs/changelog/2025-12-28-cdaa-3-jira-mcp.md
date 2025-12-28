# Changelog: CDAA-3 JIRA MCP Server

**Date**: 2025-12-28
**Author**: Antigravity Agent
**JIRA**: CDAA-3

## Added
- `src/jira_mcp_server.py`: MCP Server implementation wrapping `jira-dev-ai-automation`.
- `docs/jira_mcp_setup.md`: Setup and usage documentation.
- `tests/verify_jira_mcp.py`: Verification script.

## Changed
- `README.md`: Added instructions for JIRA MCP Server.
- Dependency: Added `mcp` to environment.

## Technical Details
- Reuse of `jira-dev-ai-automation` library via submodule integration.
- FastMCP server exposing `fetch`, `comment`, and `transition` tools.
