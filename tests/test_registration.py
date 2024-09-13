"""Module for registration tests."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.test import client as test_client


class TestRegistration(TestCase):
    """Class for registration tests."""

    _url = '/register/'
    _valid_creds = {
        'username': 'user',
        'password1': 'new_password123',
        'password2': 'new_password123',
        'first_name': 'New Name',
        'last_name': 'New Surname',
        'email': 'new_email@example.com',
    }

    def setUp(self):
        """Set up test parameters."""
        self.client = test_client.Client()

    def test_invalid(self):
        """Test with invalid credentials."""
        invalid_creds = self._valid_creds.copy()
        invalid_creds['password1'] = 'abc'
        self.client.post(self._url, invalid_creds)
        self.assertEqual(len(User.objects.filter(username='user')), 0)

    def test_valid(self):
        """Test with valid credentials."""
        self.client.post(self._url, self._valid_creds)
        self.assertEqual(len(User.objects.filter(username='user')), 1)
