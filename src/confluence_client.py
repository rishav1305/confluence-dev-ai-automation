import os
from atlassian import Confluence
from typing import Optional

class ConfluenceClient:
    """
    A wrapper around the atlassian-python-api Confluence client
    to handle authentication and basic page operations.
    """

    def __init__(self, url: Optional[str] = None, username: Optional[str] = None, api_token: Optional[str] = None):
        self.url = url or os.environ.get("CONFLUENCE_URL")
        self.username = username or os.environ.get("CONFLUENCE_USERNAME")
        self.api_token = api_token or os.environ.get("CONFLUENCE_API_TOKEN")

        if not all([self.url, self.username, self.api_token]):
            raise ValueError("Confluence URL, Username, and API Token are required.")

        self.confluence = Confluence(
            url=self.url,
            username=self.username,
            password=self.api_token,
            cloud=True
        )

    def page_exists(self, space: str, title: str) -> bool:
        """Checks if a page exists in the given space."""
        return self.confluence.page_exists(space, title)

    def create_page(self, space: str, title: str, body: str, parent_id: Optional[str] = None) -> dict:
        """Creates a new page in the given space."""
        status = self.confluence.create_page(
            space=space,
            title=title,
            body=body,
            parent_id=parent_id,
            representation='storage'
        )
        return status

    def update_page(self, page_id: str, title: str, body: str) -> dict:
        """Updates an existing page."""
        status = self.confluence.update_page(
            page_id=page_id,
            title=title,
            body=body,
            representation='storage'
        )
        return status

    def get_page_id(self, space: str, title: str) -> Optional[str]:
        """Retrieves the page ID for a given page title in a space."""
        page = self.confluence.get_page_by_title(space=space, title=title)
        if page:
            return page.get('id')
        return None
