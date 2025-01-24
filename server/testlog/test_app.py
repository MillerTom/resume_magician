
import unittest
from django.test import Client

class TestLogView(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.url = "/log/"

    def test_log_success(self):
        response = self.client.post(
            self.url,
            {
                "Message": "Test log message.",
                "Severity": "INFO",
                "ConsumingApp": "LinkedInScraper"
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Log sent successfully.", str(response.content))
    
    def test_log_missing_parameters(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing parameters.", str(response.content))
