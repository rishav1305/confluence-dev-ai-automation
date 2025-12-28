
# CDAA-2: Build an MCP server for this

**Status**: PO VALIDATION
**Summary**: Build an MCP server for this
**Description**: 
Built a Model Context Protocol (MCP) server for Confluence.
This server allows AI agents to Programmatically interact with Confluence.

## Features
- **SSE Transport**: Runs on port 8081 via Server-Sent Events.
- **Tools Exposed**:
    - `get_page`: Retrieve page content (storage format).
    - `create_page`: Create new pages.
    - `update_page`: Update existing pages.
    - `search_pages`: Search using CQL.
    - `get_page_id`: Helper to find page IDs.

## Technical Details
- **Implementation**: `src/confluence_mcp_server.py` using `mcp.server.fastmcp`.
- **Backend**: `src/confluence_client.py` using `atlassian-python-api`.
- **Dependencies**: `mcp`, `atlassian-python-api`.

## Usage
Run the server:
```bash
python -m src.confluence_mcp_server --transport sse --port 8081
```

## Verification
Verified using a custom client script connecting to `http://127.0.0.1:8081/sse`.
Search and data retrieval confirmed working.
