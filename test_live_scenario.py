import asyncio
import sys
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client

async def run():
    url = "http://0.0.0.0:8080/sse"
    issue_key = "CDAA-3"
    
    print(f"Connecting to {url}...")
    
    async with sse_client(url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 1. Read Description
            print(f"\n1. Fetching Issue {issue_key}...")
            # Tool name: get_issue
            result_get = await session.call_tool("get_issue", arguments={"issue_key": issue_key})
            content_get = result_get.content[0].text
            print(f"Result (First 100 chars): {content_get[:100]}...")
            
            # Simple check
            if "Issue not found" in content_get:
                print("Failed to find issue!")
                return

            # 2. Add Comment
            print(f"\n2. Adding Comment to {issue_key}...")
            comment_text = "Live Verification: Testing Add Comment via SSE Server."
            # Tool name: add_comment
            result_comment = await session.call_tool("add_comment", arguments={"issue_key": issue_key, "comment_text": comment_text})
            print(f"Result: {result_comment.content[0].text}")

            # 3. Change Status to Done
            print(f"\n3. Transitioning {issue_key} to DONE...")
            # Tool name: transition_issue
            # Note: Status names are case sensitive in JIRA usually, but our service handles lower.
            # Assuming 'Done' is the target.
            result_trans = await session.call_tool("transition_issue", arguments={"issue_key": issue_key, "status_name": "Done"})
            print(f"Result: {result_trans.content[0].text}")

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
