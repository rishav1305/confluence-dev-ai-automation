# Changelog: CDAA-1 Confluence Automation

## Features
- **Confluence Client**: Implemented a python client (`src/confluence_client.py`) to interact with Confluence Cloud.
- **Doc Generator**: Added a CLI tool (`src/doc_generator.py`) to create and update pages.
- **Dependencies**: Added `atlassian-python-api`.

## Configuration
- Requires `CONFLUENCE_URL`, `CONFLUENCE_USERNAME`, `CONFLUENCE_API_TOKEN` in `.env`.

## Verification
- Unit tests added in `tests/test_confluence_client.py`.
- Verified logic with mocks. Live verification pending credentials updates.
