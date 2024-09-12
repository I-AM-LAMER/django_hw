"""Module for model and client tests."""

from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from fitness_app.models import *
from django.db.utils import DataError

MAX_AMOUNT_OF_MONEY = 10000000

def create_model_test(model_class, valid_attrs: dict, invalid_attrs: tuple[dict] = None, repl_factor: int = 1):
    """Create a model test class.

    Args:
        model_class (class): The model class to test.
        valid_attrs (dict): Valid attribute values.
        invalid_attrs (tuple[dict], optional): Invalid attribute values. Defaults to None.
        repl_factor (int, optional): Replacement factor. Defaults to 1.

    Returns:
        class: A TestCase subclass for the model.
    """
    class ModelTest(TestCase):

        def setUp(self) -> None:
            """Set up the test environment."""
            self.address_obj = Address.objects.create(city_name='A',
                                            street_name='B',
                                            house_number=1,
                                            apartment_number=2, 
                                            body='A')
            self.gym_obj = Gym.objects.create(gym_name="A", address=self.address_obj)
            self.coach_obj = Coach.objects.create(first_name='A', last_name='B', spec='C')

        def test_unsuccessful_creation(self):
            """Test unsuccessful creation with invalid attributes."""
            if invalid_attrs:
                for invalid_attr in invalid_attrs:
                    with self.assertRaises(invalid_attr['exception']):
                        del invalid_attr['exception']
                        if model_class == Subscription:
                            invalid_attr['gym'] = self.gym_obj
                        if model_class == Gym:
                            invalid_attr['address'] = self.address_obj
                        if model_class == Certificate:
                            invalid_attr['coach'] = self.coach_obj
                        instance = model_class.objects.create(**invalid_attr)
                        instance.full_clean()
                        instance.save()

        def test_successful_creation(self):
            """Test successful creation with valid attributes."""
            if model_class == Gym:
                valid_attrs['address'] = self.address_obj
            if model_class == Certificate:
                valid_attrs['coach'] = self.coach_obj
            if model_class == Subscription:
                valid_attrs['gym'] = self.gym_obj
            model_class.objects.create(**valid_attrs)

    return ModelTest

GymModelTest = create_model_test(
    Gym,
    {'gym_name': 'A'},
    (
        {'gym_name': 'A'*101, 'exception': DataError},
    )
)

CoachModelTest = create_model_test(
    Coach,
    {'first_name': 'A', 'last_name': 'B', 'spec': 'C'},
    (
        {'first_name':'A'* 51, 'last_name': 'B', 'spec': 'C', 'exception': DataError},
    )
)

SubscriptionModelTest = create_model_test(
    Subscription,
    {'price': 100, 'expire_date': date.today(), 'description': 'some_desc'},
    (
        {'price': -1, 'expire_date': date.today(), 'description': 'some_desc', 'exception': ValidationError},
        {'price': 100, 'expire_date': date(2000, 1, 1), 'description': 'some_desc', 'exception': ValidationError},
    )
)

AddressModelTest = create_model_test(
    Address,
    {'city_name': 'A', 'street_name': 'B', 'house_number': 1, 'apartment_number': 1, 'body': 'A'},
    (
        {'city_name': 'A', 'street_name': 'B', 'house_number': -1, 'apartment_number': 1, 'body': 'A', 'exception': ValidationError},
        {'city_name': 'A', 'street_name': 'B', 'house_number': 1, 'apartment_number': -1, 'body': 'A', 'exception': ValidationError},
        {'city_name': 'A', 'street_name': 'B', 'house_number': 1, 'apartment_number': 1, 'body': 'abcd', 'exception': ValidationError},
    )
)

class ClientTest(TestCase):
    """Class for client tests."""

    def setUp(self) -> None:
        """Set up test parameters."""
        self.user = User.objects.create(username='abc', first_name='abc', last_name='abc', password='abc')

    def test_invalid(self):
        """Test invalid inputs."""
        with self.assertRaises(ValidationError):
            Client.objects.create(user=self.user, net_worth=-1)
            Client.objects.create(user=self.user, net_worth=MAX_AMOUNT_OF_MONEY)

    def test_create_and_str(self):
        """Test creation and string representation."""
        self.assertEqual(str(Client.objects.create(user=self.user)), 'abc (abc abc)')
