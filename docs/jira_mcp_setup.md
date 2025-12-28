# JIRA MCP Server Setup

This project includes a Model Context Protocol (MCP) Server to interact with JIRA using the `jira-dev-ai-automation` library.

## Prerequisites

1. **Python 3.10+**
2. **JIRA Credentials** in a `.env` file:
   ```env
   JIRA_URL=https://your-domain.atlassian.net
   JIRA_USER_EMAIL=your-email@example.com
   JIRA_API_TOKEN=your-api-token
   JIRA_PROJECT_KEY=CDAA
   ```

## Installation

1. Clone the repository (if not already done).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # OR
   pip install mcp requests python-dotenv
   ```
3. Ensure the submodule `jira-dev-ai-automation` is present (or cloned).

## Running the Server

Run the MCP server using Python:

```bash
python src/jira_mcp_server.py
```

This starts the server on stdio. You can connect to it using any MCP client (e.g., Claude Desktop, Zed, or a custom inspector).

## Available Tools

- **`fetch_jira_issue(issue_key)`**: 
  - Fetches and returns the summary, status, assignee, and description of a JIRA issue.
  
- **`add_jira_comment(issue_key, comment)`**:
  - Adds a text comment to the specified issue.
  
- **`transition_jira_issue(issue_key, status)`**:
  - Moves the issue to a new status (e.g., "In Progress", "Done").

## Troubleshooting

- **ImportError**: Make sure `jira-dev-ai-automation` is in the root directory or `PYTHONPATH`.
- **Credential Errors**: Check your `.env` file and ensure the API token is valid.
