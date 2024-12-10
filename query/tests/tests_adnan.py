from django.test import TestCase
from unittest import mock
from query.query import episode_details

mock_query = mock.MagicMock()
mock_simplify_result = mock.MagicMock()


# Create your tests here.
@mock.patch("query.query.__query", mock_query)
@mock.patch("query.query.__simplify_query_result", mock_simplify_result)
class test_details_query(TestCase):

    def tearDown(self):
        mock_query.reset_mock()
        mock_simplify_result.reset_mock()

    def test_details_successful(self):
        """Q1, R1"""
        mock_query.side_effect = [1]
        mock_simplify_result.side_effect = [1]

        result = episode_details("squidward")
        self.assertEqual(result, 1)
        mock_query.assert_called_once()
        mock_simplify_result.assert_called_once

    def test_details_no_result(self):
        """Q1, R2"""
        mock_query.side_effect = [None]
        mock_simplify_result.side_effect = [ValueError]

        with self.assertRaises(ValueError):
            episode_details("squidward")
        mock_query.assert_called_once()
        mock_simplify_result.assert_not_called()

    def test_details_failed_query(self):
        """Q2, R2"""
        mock_query.side_effect = [Exception]
        mock_simplify_result.side_effect = [ValueError]

        with self.assertRaises(ValueError):
            episode_details("squidward")
        mock_query.assert_called_once()
        mock_simplify_result.assert_not_called()
