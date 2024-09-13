from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from datetime import date
from json import loads

from fitness_app.models import *


def create_viewset_test(model_class, url: str, creation_attrs: dict):
    """Create a test case for a view set.

    Args:
        model_class (class): The model class to test.
        url (str): The URL endpoint for the view set.
        creation_attrs (dict): Attributes needed to create objects of the model class.
    """
    class ViewSetTest(TestCase):

        def setUp(self):
            """Set up the test environment."""
            self.client = APIClient()
            self.address_obj = Address.objects.create(city_name='A', street_name='B', house_number=1, apartment_number=2, body='A')
            self.gym_obj = Gym.objects.create(gym_name='A', address=self.address_obj)
            self.coach_obj = Coach.objects.create(first_name='A', last_name='B', spec='C')
            self.user = User.objects.create_user(username='user', password='user')
            self.superuser = User.objects.create_user(
                username='superuser', password='superuser', is_superuser=True,
            )
            self.client_obj = Client.objects.create(user=self.user, net_worth=99999)
            self.user_token = Token.objects.create(user=self.user)
            self.superuser_token = Token.objects.create(user=self.superuser)

        def get(self, user: User, token: Token):
            """Perform a GET request to the view set.

            Args:
                user (User): The authenticated user.
                token (Token): The authentication token.
            """
            self.client.force_authenticate(user=user, token=token)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_get_by_user(self):
            """Test GET request for regular users."""
            self.get(self.user, self.user_token)

        def test_get_by_superuser(self):
            """Test GET request for superusers."""
            self.get(self.superuser, self.superuser_token)

        def manage(self, user: User, token: Token, post_status: int, put_status: int, delete_status: int):
            """Perform CRUD operations on objects.

            Args:
                user (User): The authenticated user.
                token (Token): The authentication token.
                post_status (int): Expected POST status code.
                put_status (int): Expected PUT status code.
                delete_status (int): Expected DELETE status code.
            """
            self.client.force_authenticate(user=user, token=token)

            # Add model-specific attributes
            if model_class == Gym:
                creation_attrs['coaches'] = [
                    f'{self.coach_obj.id}' 
                    ]
                creation_attrs['address'] = f'{self.address_obj.id}'
            if model_class == Coach:
                creation_attrs['gyms'] = [
                    f'{self.gym_obj.id}'
                    ]
            if model_class == Certificate:
                creation_attrs['coach'] = f'{self.coach_obj.id}'

            if model_class == Subscription:
                creation_attrs['clients'] = [
                    f'{self.client_obj.id}'
                    ]
                creation_attrs['gym'] = f'{self.gym_obj.id}'

            response = self.client.post(url, creation_attrs)
            self.assertEqual(response.status_code, post_status)

            if model_class == Gym:
                creation_attrs['first_name'] = 'test'

            try:
                response = self.client.put(f'{url}{loads(response.content)['id']}/', creation_attrs)
                self.assertEqual(response.status_code, put_status)

                response = self.client.delete(f'{url}{loads(response.content)['id']}/')
                self.assertEqual(response.status_code, delete_status)
            except KeyError:
                pass
        def test_manage_user(self):
            """Test CRUD operations for regular users."""
            self.manage(
                user=self.user, token=self.user_token,
                post_status=status.HTTP_403_FORBIDDEN,
                put_status=status.HTTP_403_FORBIDDEN,
                delete_status=status.HTTP_403_FORBIDDEN,
            )

        def test_manage_superuser(self):
            """Test CRUD operations for superusers."""
            self.manage(
                user=self.superuser, token=self.superuser_token,
                post_status=status.HTTP_201_CREATED,
                put_status=status.HTTP_200_OK,
                delete_status=status.HTTP_204_NO_CONTENT,
            )

    return ViewSetTest

GymViewSetTest = create_viewset_test(
    Gym, '/rest/gym/',
    {'gym_name': 'A'}
)

CoachViewSetTest = create_viewset_test(
    Coach, '/rest/coach/',
    {'first_name': 'A', 'last_name': 'B', 'spec': 'C'}
)

CertificateViewSetTest = create_viewset_test(
    Certificate, '/rest/certificate/',
    {'certf_name': 'A', 'description': 'B'}
)

AddressViewSetTest = create_viewset_test(
    Address, '/rest/address/',
    {"city_name":'A', "street_name":'B', "house_number":1, "apartment_number":2, "body":'A'}
)

SubscriptionViewSetTest = create_viewset_test(
    Subscription, '/rest/subscription/',
    {'price': 0, 'expire_date': date(2050, 1, 1), 'description': 'some_desc'}
)