# JIRA MCP Integration

This project integrates with JIRA via a separate **Model Context Protocol (MCP)** server.

## Overview
Instead of directly importing JIRA libraries, we use an MCP client to communicate with the `jira-dev-ai-automation` server.

## Connection Details
- **Type**: SSE (Server-Sent Events)
- **URL**: `http://0.0.0.0:8080/sse`

### Configuration
Ensure your MCP client (e.g., Claude Desktop, Cursor, or custom script) is configured to connect to the above SSE endpoint.

## Available Tools
The server exposes the following tools:

| Tool | Description |
|------|-------------|
| `get_issue` | Get details of a JIRA issue (Summary, Status, Description). |
| `add_comment` | Add a comment to a JIRA issue. |
| `transition_issue` | Transition a JIRA issue to a new status (e.g., 'Done'). |
| `create_issue` | Create a new JIRA issue. |
| `search_tasks` | Search for issues using JQL. |

## Verification
To verify the connection, ensure the JIRA MCP server is running:
```bash
# In jira-dev-ai-automation repo
python -m src.mcp_server --transport sse --host 0.0.0.0 --port 8080
```
Then run a client connection test.
