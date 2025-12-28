
import unittest
from unittest.mock import MagicMock, patch
from src.confluence_mcp_server import get_page, create_page, update_page

class TestConfluenceMCPServer(unittest.TestCase):

    @patch('src.confluence_mcp_server.get_client')
    def test_get_page(self, mock_get_client):
        # Setup mock
        mock_client = MagicMock()
        mock_client.get_page.return_value = {"id": "123", "title": "Test Page"}
        mock_get_client.return_value = mock_client

        # Execute
        result = get_page("123")

        # Verify
        mock_client.get_page.assert_called_once_with("123")
        self.assertIn("Test Page", result)

    @patch('src.confluence_mcp_server.get_client')
    def test_create_page(self, mock_get_client):
        # Setup mock
        mock_client = MagicMock()
        mock_client.create_page.return_value = {"id": "456", "title": "New Page"}
        mock_get_client.return_value = mock_client

        # Execute
        result = create_page("DS", "New Page", "<p>Body</p>")

        # Verify
        mock_client.create_page.assert_called_once_with("DS", "New Page", "<p>Body</p>", None)
        self.assertIn("New Page", result)

    @patch('src.confluence_mcp_server.get_client')
    def test_update_page(self, mock_get_client):
        # Setup mock
        mock_client = MagicMock()
        mock_client.update_page.return_value = {"id": "123", "version": 2}
        mock_get_client.return_value = mock_client

        # Execute
        result = update_page("123", "Updated Title", "<p>New Body</p>")

        # Verify
        mock_client.update_page.assert_called_once_with("123", "Updated Title", "<p>New Body</p>")
        self.assertIn("version", result)

if __name__ == '__main__':
    unittest.main()
