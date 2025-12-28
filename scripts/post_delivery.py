import sys
import os
import importlib.util

# Setup
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
server_path = os.path.join(root_dir, "src", "jira_mcp_server.py")

# Load MCP Server Module
spec = importlib.util.spec_from_file_location("jira_mcp_server", server_path)
jira_mcp_server = importlib.util.module_from_spec(spec)
sys.modules["jira_mcp_server"] = jira_mcp_server
spec.loader.exec_module(jira_mcp_server)

issue_key = "CDAA-3"

# 1. Post QA Report
qa_comment = """
h1. QA Report - CDAA-3
h2. Implementation
* JIRA MCP Server created in `src/jira_mcp_server.py`
* Wraps `jira-dev-ai-automation` library.
* Tools: Fetch, Comment, Transition.

h2. Verification
* Verified Fetch Tool: Success (Retrieved details).
* Verified Comment Tool: Success (Adding this comment).
* Verified Transition Tool: Pending.

h2. Artifacts
* `docs/jira_mcp_setup.md` created.
* `README.md` updated.
"""

print(f"Posting QA Comment to {issue_key}...")
res = jira_mcp_server.add_jira_comment(issue_key, qa_comment)
print(res)

# 2. Transition to PO Validation
# Status flow: Ready for Dev -> In Progress -> QA Testing -> PO Validation
# Ensure we are in correct state or just try moving.
print(f"Transitioning {issue_key} to PO VALIDATION...")
# First try 'In Progress' just in case
jira_mcp_server.transition_jira_issue(issue_key, "In Progress")
# Then 'QA Testing'
jira_mcp_server.transition_jira_issue(issue_key, "QA TESTING")
# Then 'PO Validation'
res_trans = jira_mcp_server.transition_jira_issue(issue_key, "PO VALIDATION")
print(res_trans)
