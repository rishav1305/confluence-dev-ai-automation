import unittest
from unittest.mock import MagicMock, patch
from src.confluence_client import ConfluenceClient

class TestConfluenceClient(unittest.TestCase):
    
    def setUp(self):
        # Mock environment variables
        self.env_patcher = patch.dict('os.environ', {
            'CONFLUENCE_URL': 'https://test.atlassian.net',
            'CONFLUENCE_USERNAME': 'test@example.com',
            'CONFLUENCE_API_TOKEN': 'test-token'
        })
        self.env_patcher.start()

    def tearDown(self):
        self.env_patcher.stop()

    @patch('src.confluence_client.Confluence')
    def test_init_success(self, mock_confluence):
        client = ConfluenceClient()
        self.assertIsNotNone(client)
        mock_confluence.assert_called_once_with(
            url='https://test.atlassian.net',
            username='test@example.com',
            password='test-token',
            cloud=True
        )

    @patch('src.confluence_client.Confluence')
    def test_init_missing_creds(self, mock_confluence):
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(ValueError):
                ConfluenceClient()

    @patch('src.confluence_client.Confluence')
    def test_page_exists(self, mock_confluence_cls):
        mock_instance = mock_confluence_cls.return_value
        mock_instance.page_exists.return_value = True
        
        client = ConfluenceClient()
        result = client.page_exists("TEST", "Test Page")
        
        self.assertTrue(result)
        mock_instance.page_exists.assert_called_with("TEST", "Test Page")

    @patch('src.confluence_client.Confluence')
    def test_create_page(self, mock_confluence_cls):
        mock_instance = mock_confluence_cls.return_value
        mock_instance.create_page.return_value = {'id': '12345'}
        
        client = ConfluenceClient()
        result = client.create_page("TEST", "New Page", "Content")
        
        self.assertEqual(result, {'id': '12345'})
        mock_instance.create_page.assert_called_with(
            space="TEST",
            title="New Page",
            body="Content",
            parent_id=None,
            representation='storage'
        )

    @patch('src.confluence_client.Confluence')
    def test_update_page(self, mock_confluence_cls):
        mock_instance = mock_confluence_cls.return_value
        mock_instance.update_page.return_value = {'id': '123'}
        
        client = ConfluenceClient()
        result = client.update_page("123", "Updated Title", "New Content")
        
        mock_instance.update_page.assert_called_with(
            page_id="123",
            title="Updated Title",
            body="New Content",
            representation='storage'
        )

if __name__ == '__main__':
    unittest.main()
