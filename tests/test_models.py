from django.test import TestCase
from django.utils import timezone
from fitness_app.models import *
from fitness_app.models import Address, Coach, Gym, Certificate, GymCoach, Client, Subscription, ClientSub


class ValidatorTests(TestCase):
    def test_check_money_validator(self):
        self.assertRaises(ValidationError, check_money, -1)
        self.assertRaises(ValidationError, check_money, 10000001)
        self.assertIsNone(check_money(5000))

    def test_check_datetime_validator(self):
        future_time = timezone.now() + timezone.timedelta(days=1)
        self.assertRaises(ValidationError, check_datetime, future_time)
        self.assertIsNone(check_datetime(timezone.now()))

    def test_check_positive_validator(self):
        self.assertRaises(ValidationError, check_positive, -1)
        self.assertIsNone(check_positive(1))

    def test_check_body_validator(self):
        self.assertRaises(ValidationError, check_body, '12')
        self.assertRaises(ValidationError, check_body, 'a')
        self.assertIsNone(check_body('A'))

    def test_check_address_len_validator(self):
        self.assertRaises(ValidationError, check_address_len, 'Short')
        self.assertIsNone(check_address_len('LongerAddress'))

    def test_check_date_validator(self):
        past_date = timezone.localdate() - timezone.timedelta(days=1)
        future_date = timezone.localdate() + timezone.timedelta(days=1)
        self.assertRaises(ValidationError, check_date, past_date)
        self.assertRaises(ValidationError, check_date, future_date)
        self.assertIsNone(check_date(timezone.localdate()))
