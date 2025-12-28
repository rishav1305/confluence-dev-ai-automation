import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import json

load_dotenv()

jira_url = os.getenv("JIRA_SERVER_URL") or os.getenv("JIRA_URL")
email = os.getenv("JIRA_USER_EMAIL")
token = os.getenv("JIRA_API_TOKEN")

if not all([jira_url, email, token]):
    print("Missing JIRA credentials in .env. Checked JIRA_SERVER_URL/JIRA_URL, JIRA_USER_EMAIL, JIRA_API_TOKEN.")
    exit(1)

issue_key = "CDAA-3"
url = f"{jira_url}/rest/api/3/issue/{issue_key}"

auth = HTTPBasicAuth(email, token)
headers = {
   "Accept": "application/json"
}

print(f"Fetching {url}...")
response = requests.get(url, headers=headers, auth=auth)

if response.status_code == 200:
    data = response.json()
    fields = data.get('fields', {})
    summary = fields.get('summary', 'No Summary')
    description = fields.get('description', 'No Description')
    status = fields.get('status', {}).get('name', 'Unknown')
    
    print(f"Issue: {issue_key}")
    print(f"Summary: {summary}")
    print(f"Status: {status}")
    print("-" * 20)
    print("Description Raw:")
    print(description)
else:
    print(f"Failed to fetch issue: {response.status_code} - {response.text}")
