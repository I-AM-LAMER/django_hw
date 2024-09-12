"""Module for form tests."""

from django.contrib.auth.models import User
from django.test import TestCase

from fitness_app.forms import AddFundsForm, RegistrationForm

valid_data = {
    'username': 'abc',
    'first_name': 'abc',
    'last_name': 'abc',
    'email': 'email@email.com',
    'password1': 'fhdjsfhk',
    'password2': 'fhdjsfhk',
}

not_matching_password = valid_data.copy()
not_matching_password['password2'] = 'abc'

invalid_email = valid_data.copy()
invalid_email['email'] = 'abc'

short_password = valid_data.copy()
short_password['password1'] = 'abc'
short_password['password2'] = 'abc'

common_password = valid_data.copy()
common_password['password1'] = 'abcdef123'
common_password['password2'] = 'abcdef123'


class TestRegistrationForm(TestCase):
    """Class for testing the registration form."""

    def test_valid(self):
        """Test for valid input."""
        self.assertTrue(RegistrationForm(data=valid_data).is_valid())

    def test_not_matching_passwords(self):
        """Test for mismatching passwords."""
        self.assertFalse(RegistrationForm(data=not_matching_password).is_valid())

    def test_short_password(self):
        """Test for short password."""
        self.assertFalse(RegistrationForm(data=short_password).is_valid())

    def test_invalid_email(self):
        """Test for invalid email."""
        self.assertFalse(RegistrationForm(data=invalid_email).is_valid())

    def test_common_password(self):
        """Test for common password."""
        self.assertFalse(RegistrationForm(data=common_password).is_valid())

    def test_existing_user(self):
        """Test for existing user."""
        User.objects.create(username=valid_data['username'], password='abc')
        self.assertFalse(RegistrationForm(data=valid_data).is_valid())


class TestAddFundsForm(TestCase):
    """Class for testing the Add Funds form."""

    def test_valid(self):
        """Test for valid integer input."""
        self.assertTrue(AddFundsForm(data={'money': 100}).is_valid())

    def test_negative(self):
        """Test for negative number."""
        self.assertFalse(AddFundsForm(data={'money': -100}).is_valid())

    def test_invalid_decimal_fields(self):
        """Test for decimal field validation."""
        self.assertFalse(AddFundsForm(data={'money': 100.123}).is_valid())

    def test_valid_decimal_fields(self):
        """Test for valid decimal input."""
        self.assertTrue(AddFundsForm(data={'money': 100.12}).is_valid())

    def test_invalid_max_digits(self):
        """Test for maximum digits limit."""
        self.assertFalse(AddFundsForm(data={'money': 123456789123}).is_valid())
