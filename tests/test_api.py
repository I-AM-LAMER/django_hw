import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from fitness_app.models import Client, Gym, Coach, Subscription, Certificate, GymCoach, Address
from fitness_app.serializers import ClientSerializer, GymSerializer, SubscriptionSerializer, CoachSerializer, CertificateSerializer, GymCoachSerializer


class SerializerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create sample instances for testing
        self.user = User.objects.create(username='testuser', email='test@example.com', password='testpass')
        self.sample_client = Client.objects.create(user=self.user)
        self.sample_gym = Gym.objects.create(gym_name='Test Gym')
        self.sample_address = Address.objects.create(city_name='Sample City', street_name='Sample St.', house_number=123, apartment_number=None)
        self.sample_coach = Coach.objects.create(first_name='John', last_name='Doe', spec='Fitness')
        self.sample_subscription = Subscription.objects.create(price=500, expire_date='2025-12-31', gym=self.sample_gym)
        self.sample_certificate = Certificate.objects.create(coach=self.sample_coach, certf_name='Certification Name', description='Description')
        self.sample_gym_coach = GymCoach.objects.create(gym=self.sample_gym, coach=self.sample_coach)
    def test_create_client(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(reverse('client-list'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue('token' in response.data)


    def test_create_gym(self):
        data = {
            'gym_name': 'New Gym',
            'address': self.sample_address.id
        }
        response = self.client.post(reverse('gym-list'), data=data)
        self.assertEqual(response.status_code, 201)
