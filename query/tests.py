from django.test import TestCase
from unittest.mock import patch
import requests
from your_module import get_image_external

class GetImageExternalTest(TestCase):
    # CFG Test Path 1: Valid URL with infobox and image tag
    @patch('query.requests.get')
    def test_valid_url_with_infobox_and_image(self, mock_get):
        """
        Test for a valid URL with an infobox containing an image tag.
        IDM: Valid query (Q1), infobox present (I1), image present (T1).
        CFG Path: start -> try -> response.raise_for_status -> soup.find -> infobox.find -> return image_tag["src"]
        """
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.text = '<html><body><aside class="portable-infobox"><img src="https://static.wikia.nocookie.net/example.jpg" /></aside></body></html>'

        result = get_image_external("http://validurl.com")
        self.assertEqual(result, "https://static.wikia.nocookie.net/example.jpg")

    # CFG Test Path 2: Valid URL with infobox but no image tag
    @patch('query.requests.get')
    def test_valid_url_with_infobox_no_image(self, mock_get):
        """
        Test for a valid URL with an infobox but no image tag.
        IDM: Valid query (Q1), infobox present (I1), no image (T2).
        CFG Path: start -> try -> response.raise_for_status -> soup.find -> infobox.find -> return None
        """
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.text = '<html><body><aside class="portable-infobox"></aside></body></html>'

        result = get_image_external("http://validurl.com")
        self.assertIsNone(result)

    # CFG Test Path 3: Valid URL with no infobox
    @patch('query.requests.get')
    def test_valid_url_no_infobox(self, mock_get):
        """
        Test for a valid URL with no infobox.
        IDM: Valid query (Q1), no infobox (I2), N/A for image presence.
        CFG Path: start -> try -> response.raise_for_status -> soup.find -> return None
        """
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.text = '<html><body></body></html>'

        result = get_image_external("http://validurl.com")
        self.assertIsNone(result)

    # CFG Test Path 4: Invalid URL causing a request exception
    @patch('query.requests.get')
    def test_invalid_url(self, mock_get):
        """
        Test for an invalid URL causing an exception.
        IDM: Invalid query (Q2), N/A for infobox or image presence.
        CFG Path: start -> try -> except -> return None
        """
        mock_get.side_effect = requests.exceptions.RequestException("Invalid URL")

        result = get_image_external("http://invalidurl.com")
        self.assertIsNone(result)

    # CFG Test Path 5: Empty query
    def test_empty_query(self):
        """
        Test for an empty query.
        IDM: Empty query (Q3), N/A for infobox or image presence.
        CFG Path: start -> return None
        """
        result = get_image_external("")
        self.assertIsNone(result)
