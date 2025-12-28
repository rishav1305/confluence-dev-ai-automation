import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client

async def run():
    url = "http://0.0.0.0:8080/sse"
    issue_key = "CDAA-1"
    status_name = "In Progress"
    
    print(f"Connecting to {url}...")
    try:
        async with sse_client(url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print(f"Transitioning {issue_key} to {status_name}...")
                result = await session.call_tool("transition_issue", arguments={"issue_key": issue_key, "status_name": status_name})
                print(f"Result: {result.content[0].text}")
                
    except Exception as e:
        print(f"Failed to transition issue: {e}")

if __name__ == "__main__":
    asyncio.run(run())
