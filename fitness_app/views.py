"""
Summary.

This module contains views for the fitness application, including user registration,
subscription management, gym and coach detail pages, and other utility functions.
"""

from django.contrib.auth import decorators
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, redirect, render
from rest_framework import authentication, permissions, viewsets

from .forms import *
from .models import *
from .serializers import (AddressSerializer, CertificateSerializer,
                          CoachSerializer, GymSerializer,
                          SubscriptionSerializer)


class MyPermission(permissions.BasePermission):
    """
    Custom permission class for restricting access based on user roles.

    Attributes:
        request (WSGIRequest): The current HTTP request object.

    Returns:
        bool: True if the request should be permitted, False otherwise.
    """

    def has_permission(self, request: WSGIRequest, _):
        """
        Check if the permission should be granted for the current request.

        Args:
            request (WSGIRequest): The current HTTP request object.

        Returns:
            bool: True if the permission should be granted, False otherwise.
        """
        if request.method in set(['GET', 'OPTIONS', 'HEAD']):
            return bool(request.user and request.user.is_authenticated)
        elif request.method in set(['POST', 'DELETE', 'PUT']):
            return bool(request.user and request.user.is_superuser)
        return False


def create_viewset(model_class, serializer):
    """
    Create and return a ModelViewSet for the given model class and serializer.

    Args:
        model_class (class): The Django model class.
        serializer (class): The corresponding serializer class.

    Returns:
        viewsets.ModelViewSet: A configured ModelViewSet instance.
    """
    class ViewSet(viewsets.ModelViewSet):
        queryset = model_class.objects.all()
        serializer_class = serializer
        authentication_classes = [authentication.TokenAuthentication]
        permission_classes = [MyPermission]
    return ViewSet


CoachViewSet = create_viewset(Coach, CoachSerializer)
GymViewSet = create_viewset(Gym, GymSerializer)
AddressViewSet = create_viewset(Address, AddressSerializer)
CertificateViewSet = create_viewset(Certificate, CertificateSerializer)
SubscriptionViewSet = create_viewset(Subscription, SubscriptionSerializer)


def register(request: WSGIRequest):
    """
    Handle user registration form submission.

    Args:
        request (WSGIRequest): The current HTTP request object.

    Returns:
        HttpResponse: Render the registration template with the form.
    """
    errors = ''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(user=user)
            return redirect('login')
        else:
            errors = form.errors
    else:
        form = RegistrationForm()
    return render(
        request,
        'registration/register.html',
        {'form': form, 'errors': errors, 'request': request},
    )


def subs_page(request: WSGIRequest):
    """
    Display subscription page for authenticated users.

    Args:
        request (WSGIRequest): The current HTTP request object.

    Returns:
        HttpResponse: Render the subscriptions template.
    """
    if request.user.is_authenticated:
        user = request.user
        subs = Subscription.objects.filter(user=user)
        return render(request, 'subs.html', {'subs': subs})
    return redirect('registration/login')


def subscribe(request: WSGIRequest):
    """
    Process subscription creation or update.

    Args:
        request (WSGIRequest): The current HTTP request object.

    Returns:
        HttpResponse: Redirect to profile or display error message.
    """
    if request.method == 'POST':
        if request.user.is_authenticated:
            id_fld = request.GET.get('id')
            sub = Subscription.objects.get(id=id_fld)
            client = Client.objects.get(user=request.user)
            if client.net_worth >= sub.price:
                client.net_worth -= sub.price
                client.subs.add(sub)
                client.save()
            return redirect('profile')
    return HttpResponse('Something went wrong...')


def main_page(request: WSGIRequest):
    """
    Render the main page of the application.

    Args:
        request (WSGIRequest): The current HTTP request object.

    Returns:
        HttpResponse: Render the base template.
    """
    return render(request, 'base.html')


@decorators.login_required
def profile(request: WSGIRequest):
    """
    Display user profile information and allow fund additions.

    Args:
        request (WSGIRequest): The current HTTP request object.

    Returns:
        HttpResponse: Render the profile template.
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            client = Client.objects.filter(user=request.user).first()
            if not client:
                client = Client.objects.create(user=request.user)
        else:
            client = Client.objects.get(user=request.user)
        if client:
            if request.method == 'POST':
                form = AddFundsForm(request.POST)
                if form.is_valid():
                    money = form.cleaned_data.get('money')
                    client.net_worth += money
                    client.save()
            else:
                form = AddFundsForm()

            client_subs = Subscription.objects.filter(client=client)
            return render(
                request,
                'profile.html',
                {
                    'client': client,
                    'subs': client_subs,
                    'form': form,
                },
            )
    else:
        return redirect('register/login.html')


def gyms_page(request: WSGIRequest):
    """
    Display gym listing page.

    Args:
        request (WSGIRequest): The current HTTP request object.

    Returns:
        HttpResponse: Render the gyms template.
    """
    return render(request, 'gyms.html', {'gyms': Gym.objects.all()})


def coaches_page(request: WSGIRequest):
    """
    Display coach listing page.

    Args:
        request (WSGIRequest): The current HTTP request object.

    Returns:
        HttpResponse: Render the coaches template.
    """
    return render(request, 'coaches.html', {'coaches': Coach.objects.all})


def gym_detail_page(request: WSGIRequest, pk):
    """
    Display detailed information about a specific gym.

    Args:
        request (WSGIRequest): The current HTTP request object.
        pk (int): The primary key of the gym to display.

    Returns:
        HttpResponse: Render the gym detail template.
    """
    if request.user.is_authenticated:
        client = Client.objects.filter(user=request.user)
        if client.exists():
            client = client.first()
        else:
            return redirect('/login')
    else:
        return redirect('/login')
    gym = Gym.objects.get(id=pk)
    coaches = list(gym.coaches.all())
    subs = Subscription.objects.filter(gym=gym).all()
    address = gym.address
    return render(
        request,
        'gym.html',
        {
            'gym': gym,
            'coaches': coaches,
            'subs': subs,
            'address': address,
            'client': client,
            'client_subs': list(client.subs.all()),
        },
    )


def coach_detail_page(request: WSGIRequest, pk):
    """
    Display detailed information about a specific coach.

    Args:
        request (WSGIRequest): The current HTTP request object.
        pk (int): The primary key of the coach to display.

    Returns:
        HttpResponse: Render the coach detail template.
    """
    coach = Coach.objects.get(id=pk)
    certfs = Certificate.objects.filter(coach=coach).values_list()
    return render(request, 'coach.html', {'coach': coach, 'certfs': certfs})
