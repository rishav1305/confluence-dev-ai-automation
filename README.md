# Confluence Dev AI Automation

## JIRA MCP Server
This project provides an MCP Server to interact with JIRA. 
It wraps the `jira-dev-ai-automation` library to expose fetch, comment, and transition tools.

### Setup
1. Configure `.env` with JIRA credentials.
2. Install dependencies: `pip install mcp requests python-dotenv`.

### Running
```bash
python src/jira_mcp_server.py
```

See [docs/jira_mcp_setup.md](docs/jira_mcp_setup.md) for details.