from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from fitness_app.models import Client, Gym, Coach, Subscription
from fitness_app.views import register, subs_page, subscribe, main_page, profile, gyms_page, coaches_page, gym_detail_page, coach_detail_page

class RegisterViewTests(TestCase):
    def test_register_get_request(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_post_request(self):
        response = self.client.post(reverse('register'), {'username': 'testuser', 'email': 'test@test.com', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)  # Redirect status code


class ProfileViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='testpass')
        self.client.force_login(self.user)
        self.client.session.flush()

    def test_profile_view_requires_authentication(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_profile_view_authenticated(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)


class SubscribeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='testpass')
        self.client.force_login(self.user)
        self.client.session.flush()

    def test_subscribe_view_authenticated(self):
        # Assuming you have a subscription with id available
        response = self.client.post(reverse('subscribe'), {'id': 1})
        self.assertEqual(response.status_code, 200)  # Redirect status code after successful subscription


class GymDetailPageTests(TestCase):
    def setUp(self):
        self.gym = Gym.objects.create(gym_name='Test Gym')
        self.coach = Coach.objects.create(first_name='John', last_name='Doe', spec='Fitness')
        self.subscription = Subscription.objects.create(price=500, expire_date='2025-12-31', gym=self.gym)
        self.client.force_login(User.objects.create_user(username='testuser', email='test@test.com', password='testpass'))
        self.client.session.flush()

    def test_gym_detail_page(self):
        response = self.client.get(reverse('gym_detail_page', kwargs={'pk': self.gym.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Gym')
