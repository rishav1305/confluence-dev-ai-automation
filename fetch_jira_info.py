import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client

async def run():
    url = "http://0.0.0.0:8080/sse"
    issue_key = "CDAA-1"
    
    print(f"Connecting to {url}...")
    try:
        async with sse_client(url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print(f"Fetching Issue {issue_key}...")
                result = await session.call_tool("get_issue", arguments={"issue_key": issue_key})
                content = result.content[0].text
                print("--- START ISSUE DETAILS ---")
                print(content)
                print("--- END ISSUE DETAILS ---")
                
    except Exception as e:
        print(f"Failed to connect or fetch issue: {e}")

if __name__ == "__main__":
    asyncio.run(run())
