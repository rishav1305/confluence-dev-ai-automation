import sys
import os
import importlib.util

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
# sys.path.append(root_dir) # We don't rely on package import for server now

# Import jira_mcp_server.py by path
server_path = os.path.join(root_dir, "src", "jira_mcp_server.py")
spec = importlib.util.spec_from_file_location("jira_mcp_server", server_path)
jira_mcp_server = importlib.util.module_from_spec(spec)
sys.modules["jira_mcp_server"] = jira_mcp_server
spec.loader.exec_module(jira_mcp_server)

# Verify tools
print(f"Fetch Tool: {jira_mcp_server.fetch_jira_issue}")
print(f"Comment Tool: {jira_mcp_server.add_jira_comment}")
print(f"Transition Tool: {jira_mcp_server.transition_jira_issue}")

print("Attempting to fetch 'CDAA-3'...")
try:
    result = jira_mcp_server.fetch_jira_issue("CDAA-3")
    print(f"Result Preview: {str(result)[:100]}...")
except Exception as e:
    print(f"Execution Error: {e}")
