from mcp.server.fastmcp import FastMCP
import sys
import os

# Add jira-dev-ai-automation to path to import src
# Assuming this script is run from the root of the repo 'confluence-dev-ai-automation'
# and 'jira-dev-ai-automation' is in the root too.
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
jira_lib_path = os.path.join(root_dir, "jira-dev-ai-automation")

# Insert at 0 to prioritize submodule 'src' over local 'src' (if any ambiguity, though we want submodule here)
if jira_lib_path not in sys.path:
    sys.path.insert(0, jira_lib_path)

try:
    from src.jira_service import JiraService
except ImportError as e:
    print(f"Error importing JiraService: {e}")
    print("Make sure 'jira-dev-ai-automation' is cloned and available.")
    sys.exit(1)

# Initialize MCP Server
mcp = FastMCP("jira_mcp")
service = JiraService()

@mcp.tool()
def fetch_jira_issue(issue_key: str) -> str:
    """
    Fetch details of a JIRA issue including summary, status, description, and assignee.
    """
    try:
        # JiraService.get_issue_details prints to stdout. We verify connection first.
        # However, to capture output we might need to modify JiraService or redirect stdout.
        # But wait, the MCP tool needs to RETURN the string, not print it.
        # Checking JiraService implementation: it prints.
        # This is not ideal for MCP. 
        # I will use a simple redirect to capture the print output for now to avoid modifying the cloned library deeply.
        
        from io import StringIO
        import sys
        
        captured_output = StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output
        
        success = service.get_issue_details(issue_key)
        
        sys.stdout = original_stdout
        
        if success:
            return captured_output.getvalue()
        else:
            return f"Failed to fetch details for {issue_key}"
            
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def add_jira_comment(issue_key: str, comment: str) -> str:
    """
    Add a comment to a JIRA issue.
    """
    if service.add_comment(issue_key, comment):
        return f"Successfully added comment to {issue_key}"
    return f"Failed to add comment to {issue_key}"

@mcp.tool()
def transition_jira_issue(issue_key: str, status: str) -> str:
    """
    Transition a JIRA issue to a new status (e.g., 'In Progress', 'Done', 'PO Validation').
    """
    if service.transition_issue(issue_key, status):
        return f"Successfully transitioned {issue_key} to {status}"
    return f"Failed to transition {issue_key} to {status}"

if __name__ == "__main__":
    mcp.run()
