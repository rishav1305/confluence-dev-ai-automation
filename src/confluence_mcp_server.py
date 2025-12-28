
import asyncio
import os
import argparse
from typing import Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from src.confluence_client import ConfluenceClient

load_dotenv()

# Initialize FastMCP Server
mcp = FastMCP("confluence-server")

# Initialize Confluence Client
# We delay initialization to allow env vars to be set or injected
client: Optional[ConfluenceClient] = None

def get_client() -> ConfluenceClient:
    global client
    if not client:
        client = ConfluenceClient()
    return client

@mcp.tool()
def get_page(page_id: str) -> str:
    """
    Get full page details including body (storage format).
    Args:
        page_id: The ID of the page to retrieve.
    """
    try:
        c = get_client()
        result = c.get_page(page_id)
        return str(result)
    except Exception as e:
        return f"Error fetching page: {str(e)}"

@mcp.tool()
def create_page(space: str, title: str, body: str, parent_id: Optional[str] = None) -> str:
    """
    Create a new page in Confluence.
    Args:
        space: The space key (e.g., 'DS').
        title: The title of the page.
        body: The content of the page (storage format).
        parent_id: Optional parent page ID.
    """
    try:
        c = get_client()
        result = c.create_page(space, title, body, parent_id)
        return str(result)
    except Exception as e:
        return f"Error creating page: {str(e)}"

@mcp.tool()
def update_page(page_id: str, title: str, body: str) -> str:
    """
    Update an existing page in Confluence.
    Args:
        page_id: The ID of the page to update.
        title: The new title.
        body: The new content (storage format).
    """
    try:
        c = get_client()
        result = c.update_page(page_id, title, body)
        return str(result)
    except Exception as e:
        return f"Error updating page: {str(e)}"

@mcp.tool()
def search_pages(cql: str) -> str:
    """
    Search for pages using Confluence Query Language (CQL).
    Args:
        cql: The CQL query string (e.g., 'text ~ "meeting"').
    """
    try:
        c = get_client()
        result = c.search_pages(cql)
        return str(result)
    except Exception as e:
        return f"Error searching pages: {str(e)}"

@mcp.tool()
def get_page_id(space: str, title: str) -> str:
    """
    Get the ID of a page by space and title.
    Args:
        space: The space key.
        title: The page title.
    """
    try:
        c = get_client()
        pid = c.get_page_id(space, title)
        if pid:
            return pid
        return "Page not found"
    except Exception as e:
        return f"Error identifying page: {str(e)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", default="stdio", choices=["stdio", "sse"])
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8081)
    args = parser.parse_args()

    if args.transport == "sse":
        import uvicorn
        print(f"Starting SSE server on {args.host}:{args.port}")
        uvicorn.run(mcp.sse_app, host=args.host, port=args.port)
    else:
        mcp.run()
