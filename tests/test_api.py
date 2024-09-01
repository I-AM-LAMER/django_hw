from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from datetime import date
from json import loads

from fitness_app.models import *


def create_viewset_test(model_class, url: str, creation_attrs: dict):
    """_summary_.

    Args:
        model_class (_type_): _description_
        url (str): _description_
        creation_attrs (dict): _description_
    """
    class ViewSetTest(TestCase):

        def setUp(self):
            """_summary_."""
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
            """Получить.

            Args:
                user (User): пользователь
                token (Token): токен
            """
            self.client.force_authenticate(user=user, token=token)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_get_by_user(self):
            """Тест на метод get для обычного пользователя."""
            self.get(self.user, self.user_token)

        def test_get_by_superuser(self):
            """тест на метод get для админа."""
            self.get(self.superuser, self.superuser_token)

        def manage(self, user: User, token: Token, post_status: int, put_status: int, delete_status: int):
            """Тесты на создание, обновление и удаление объектов.

            Args:
                user (User): пользователь
                token (Token): токен
                post_status (int): пост статус код
                put_status (int): пут статус код
                delete_status (int): статус код для удаления
            """
            self.client.force_authenticate(user=user, token=token)

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

            # POST
            response = self.client.post(url, creation_attrs)
            content = loads(response.content)

            try:
                created_id = content['id']
            except KeyError:
                created_id = None

            self.assertEqual(response.status_code, post_status)

            if model_class == Coach:
                creation_attrs['first_name'] = 'test'
            
            if model_class == Gym:
                creation_attrs['gym_name'] = 'test'
            
            if model_class == Certificate:
                creation_attrs['certf_name'] = 'test'
            
            if model_class == Address:
                creation_attrs['city_name'] = 'test'
            
            if model_class == Subscription:
                creation_attrs['expire_date'] = date(2060, 10, 10)

            # PUT
            response = self.client.put(f'{url}{created_id}/', creation_attrs)
            self.assertEqual(response.status_code, put_status)

            # DELETE
            response = self.client.delete(f'{url}{created_id}/')
            self.assertEqual(response.status_code, delete_status)

        def test_manage_user(self):
            """Тест для обычного пользователя."""
            self.manage(
                user=self.user, token=self.user_token,
                post_status=status.HTTP_403_FORBIDDEN,
                put_status=status.HTTP_403_FORBIDDEN,
                delete_status=status.HTTP_403_FORBIDDEN,
            )

        def test_manage_superuser(self):
            """Тест для админа."""
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