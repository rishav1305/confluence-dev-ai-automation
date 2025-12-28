import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client

async def run():
    url = "http://0.0.0.0:8080/sse"
    issue_key = "CDAA-1"
    comment = "Implemented Confluence automation logic (Client + CLI). Unit tests passed. Ready for live verification once credentials are configured."
    
    print(f"Connecting to {url}...")
    try:
        async with sse_client(url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print(f"Adding comment to {issue_key}...")
                result = await session.call_tool("add_comment", arguments={"issue_key": issue_key, "comment_text": comment})
                print(f"Result: {result.content[0].text}")
                
                print(f"Transitioning {issue_key} to QA Testing...")
                # Assuming 'QA Testing' is the status name, or similar. If not, it might fail/stay.
                # Let's try 'QA Testing' based on rules, or check valid transitions if I could (but I can't easily).
                # Actually, standard JIRA usually has "In Progress" -> "Done" or "Review".
                # The user rules said "QA TESTING". I'll try that.
                await session.call_tool("transition_issue", arguments={"issue_key": issue_key, "status_name": "QA Testing"})
                
    except Exception as e:
        print(f"Failed to update JIRA: {e}")

if __name__ == "__main__":
    asyncio.run(run())
