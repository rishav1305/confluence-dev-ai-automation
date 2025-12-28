
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def transition_issue():
    sse_url = "http://0.0.0.0:8080/sse"
    print(f"Connecting to {sse_url}...")
    
    try:
        async with sse_client(sse_url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("Transitioning CDAA-2 to 'IN PROGRESS'...")
                result = await session.call_tool("transition_issue", {
                    "issue_key": "CDAA-2", 
                    "status_name": "In Progress"
                })
                
                for content in result.content:
                    if content.type == "text":
                        print(f"Result: {content.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(transition_issue())
