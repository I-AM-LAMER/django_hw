from django.contrib.auth import decorators
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, redirect, render
from rest_framework import authentication, permissions, viewsets

from .forms import *
from .models import *
from .serializers import (CertificateSerializer, ClientSerializer,
                          CoachSerializer, GymCoachSerializer, GymSerializer,
                          SubscriptionSerializer)


class MyPermission(permissions.BasePermission):
    def has_permission(self, request: WSGIRequest, _):
        if request.method in ('GET', 'OPTIONS', 'HEAD'):
            return bool(request.user and request.user.is_authenticated)
        elif request.method in ('POST', 'DELETE', 'PUT'):
            return bool(request.user and request.user.is_superuser)
        return False


def create_viewset(model_class, serializer):
    class ViewSet(viewsets.ModelViewSet):
        queryset = model_class.objects.all()
        serializer_class = serializer
        authentication_classes = [authentication.TokenAuthentication]
        permission_classes = [MyPermission]
    return ViewSet

CoachViewSet = create_viewset(Coach, CoachSerializer)
ClientViewSet = create_viewset(Client, ClientSerializer)
GymViewSet = create_viewset(Gym, GymSerializer)
GymCoachViewSet = create_viewset(GymCoach, GymCoachSerializer)
CertificateViewSet = create_viewset(Certificate, CertificateSerializer)
SubscriptionViewSet = create_viewset(Subscription, SubscriptionSerializer)

def register(request: WSGIRequest):
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
    if request.user.is_authenticated:
        user = request.user
        subs = Subscription.objects.filter(user=user)
        return render(request, 'subs.html', {'subs': subs})
    else:
        return redirect('registration/login')

def subscribe(request: WSGIRequest):
    if request.method == 'POST':
        if request.user.is_authenticated:
            id = request.GET.get('id')
            sub = Subscription.objects.get(id=id)
            client = Client.objects.get(user=request.user)
            if client.net_worth >= sub.price:            
                client.net_worth -= sub.price
                client.subs.add(sub)
                client.save()
            return redirect('profile')
    return HttpResponse('Something went wrong...')

def main_page(request: WSGIRequest):
    return render(request, 'base.html')

@decorators.login_required
def profile(request: WSGIRequest):
    if request.user.is_authenticated:
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
            return render(request, 'profile.html', {'client': client, 'subs': client_subs, 'form': form})
    else:
        return redirect('register/login.html')

def gyms_page(request: WSGIRequest):
    return render(request, 'gyms.html', {'gyms': Gym.objects.all()})

def coaches_page(request: WSGIRequest):
    return render(request, 'coaches.html', {'coaches': Coach.objects.all})

def gym_detail_page(request: WSGIRequest, pk):
    if request.user.is_authenticated:
        client = Client.objects.filter(user=request.user)
        if client.exists():
            client = client.first()
    else:
        return redirect('/login')
    gym = Gym.objects.get(id=pk)
    coaches = [coach for coach in gym.coaches.all()]
    subs = Subscription.objects.filter(gym=gym).all()
    client_subs = client.subs.all()
    print()
    address = gym.address
    return render(request, 'gym.html', {'gym': gym, 'coaches': coaches, 'subs': subs, 'address': address, 'client': client, 'client_subs':client_subs})

def coach_detail_page(request: WSGIRequest, pk):
    coach = Coach.objects.get(id=pk)
    certfs = Certificate.objects.filter(coach=coach).values_list()
    return render(request, 'coach.html', {'coach': coach, 'certfs': certfs})