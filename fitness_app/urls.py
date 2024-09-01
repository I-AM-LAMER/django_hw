from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'gym', GymViewSet)
router.register(r'coach', CoachViewSet)
router.register(r'certificate', CertificateViewSet)
router.register(r'subscription', SubscriptionViewSet)
router.register(r'address', AddressViewSet)
# router.register(r'Client', ClientViewSet)

urlpatterns = [
    path('', main_page, name='homepage'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/register/', register, name='register'),
    path('rest/', include(router.urls)),
    path('gyms/', gyms_page),
    path('coaches/', coaches_page),
    path('coaches/<uuid:pk>/', coach_detail_page, name='coach'),
    path('gyms/<uuid:pk>/', gym_detail_page, name='gym'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('subscribe/', subscribe, name='subscribe')
]