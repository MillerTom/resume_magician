from django.urls import reverse
from django.test import TestCase
from unittest.mock import patch
from scraper.models import Scraper, Configuration


class ScraperStartViewTest(TestCase):
    def setUp(self):
        # Create a mock Scraper object
        self.scraper = Scraper.objects.create(
            name='ZipRecruiter',
            actor_id='vQO5g45mnm8jwognj',
            actor_name='memo23/apify-ziprecruiter-scraper',
            is_active=True,
        )

        # Create associated Configuration object
        self.configuration = Configuration.objects.create(
            scraper=self.scraper,
            skill='D365 CRM Developer',
            url='https://www.ziprecruiter.com/jobs-search?search=.net+c%23&location=Remote+%28USA%29&days=1',
            priority=3,
            days=1,
            is_active=True,
        )

        # Define url and valid data
        self.url = reverse('start_scraping')
        self.valid_data = {
            'numberOfDays': 1,
            'appConsuming': 'ZipRecruiter'
        }


    @patch('scraper.views.run_actor')  # Mock the run_actor function
    def test_post_success(self, mock_run_actor):
        # Ensure the mock is called with the expected arguments
        mock_run_actor.return_value = None  # Mock the function's return value

        print(self.url)
        # Make the POST request with valid data
        response = self.client.post(self.url, data=self.valid_data, format='json')

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'success')

        # Check the response content
        self.assertEqual(
            response.data,
            {
                'status': 'success',
                'message': 'successfully scheduled tasks. Wait for a moment to get the results.',
            },
        )

        # # Ensure run_actor was called for each active scraper and configuration
        # mock_run_actor.assert_called_once_with(self.scraper, self.configuration)


    def test_post_invalid_data(self):
        # Make the POST request with invalid data
        response = self.client.post(self.url, data={}, format='json')

        # Check that the response status code is 400
        self.assertEqual(response.status_code, 400)