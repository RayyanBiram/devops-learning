import unittest
from unittest.mock import patch
from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_welcome_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_welcome_contains_expected_text(self):
        response = self.client.get('/')
        self.assertIn(b'Rayyan is always watching', response.data)

    @patch('app.cache.incr')
    def test_count_increments_and_displays(self, mock_incr):
        mock_incr.return_value = 5
        response = self.client.get('/count')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'5', response.data)
        mock_incr.assert_called_once_with('visits')


if __name__ == '__main__':
    unittest.main()