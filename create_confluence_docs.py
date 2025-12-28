
import asyncio
import os
from mcp import ClientSession
from mcp.client.sse import sse_client
from src.md_converter import markdown_to_confluence

# Configuration
CONF_MCP_URL = "http://127.0.0.1:8081/sse"
JIRA_MCP_URL = "http://0.0.0.0:8080/sse"
SPACE_KEY = "CDAA"
SPACE_NAME = "Confluence Dev AI Automation"

async def create_docs():
    print(f"Connecting to Confluence MCP at {CONF_MCP_URL}...")
    
    # 1. Create Space (if not exists)
    try:
        async with sse_client(CONF_MCP_URL) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print(f"Creating Space '{SPACE_KEY}'...")
                # Note: create_space might fail if it already exists, checking output not strict here
                res = await session.call_tool("create_space", {"key": SPACE_KEY, "name": SPACE_NAME})
                print(f"Space Creation Result: {res}")

                # 2. Process README.md
                readme_path = "README.md"
                if os.path.exists(readme_path):
                    with open(readme_path, "r") as f:
                        md_content = f.read()
                    
                    storage_format = markdown_to_confluence(md_content)
                    print("Creating 'README' page...")
                    page_res = await session.call_tool("create_page", {
                        "space": SPACE_KEY,
                        "title": "README",
                        "body": storage_format
                    })
                    print(f"Page Result: {page_res}")
                
                # 3. Process docs/ folder
                docs_dir = "docs"
                for filename in os.listdir(docs_dir):
                    if filename.endswith(".md"):
                        file_path = os.path.join(docs_dir, filename)
                        with open(file_path, "r") as f:
                            content = f.read()
                        
                        title = filename.replace(".md", "")
                        storage_format = markdown_to_confluence(content)
                        
                        print(f"Creating page '{title}'...")
                        page_res = await session.call_tool("create_page", {
                            "space": SPACE_KEY,
                            "title": title,
                            "body": storage_format
                        })
                        print(f"Page Result: {page_res}")

    except Exception as e:
        print(f"Confluence Operations Error: {e}")
        return

    # 4. Link to JIRA
    # Assuming the Base URL is standard, we construct the link manually for the comment
    # Ideal: Parse page creation result to get ID and link.
    # For now, we'll formulate a generic link to the space.
    # space_link = f"{os.environ.get('CONFLUENCE_URL')}/display/{SPACE_KEY}"
    
    print(f"Connecting to JIRA MCP at {JIRA_MCP_URL}...")
    try:
        async with sse_client(JIRA_MCP_URL) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                comment = f"Created documentation in Confluence Space: {SPACE_KEY}. Pages: README, docs/*.md"
                print("Adding JIRA comment...")
                await session.call_tool("add_comment", {
                    "issue_key": "CDAA-2",
                    "comment_text": comment
                })
                print("JIRA updated.")

    except Exception as e:
        print(f"JIRA Operations Error: {e}")

if __name__ == "__main__":
    asyncio.run(create_docs())
