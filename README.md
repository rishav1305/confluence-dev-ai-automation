# confluence-dev-ai-automation

## JIRA Integration
This project uses an external JIRA MCP Server for issue management.
See [docs/jira_mcp_usage.md](docs/jira_mcp_usage.md) for connection details and available tools.

## Confluence Automation
This project includes tools to automate Confluence page creation.

### Setup
1.  Ensure you have `atlassian-python-api` installed: `pip install atlassian-python-api`
2.  Add the following to your `.env` file:
    ```
    CONFLUENCE_URL=https://your-domain.atlassian.net
    CONFLUENCE_USERNAME=your-email@example.com
    CONFLUENCE_API_TOKEN=your-api-token
    ```

### Usage
Generate a page using the script:
```bash
python3 src/doc_generator.py --space "SPACE_KEY" --title "Page Title" --content "<h1>Hello World</h1><p>Content</p>"
```

### Confluence MCP Server
Run a local MCP server to expose Confluence to AI agents via SSE:
```bash
# Uses port 8081 by default
python -m src.confluence_mcp_server --transport sse --port 8081
```