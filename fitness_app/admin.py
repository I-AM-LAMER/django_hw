"""_summary_."""

from django.contrib import admin

from .forms import CertificateForm, CoachForm, GymForm
from .models import Address, Certificate, Coach, Gym, GymCoach, Subscription

# inlines


class GymCoachInline(admin.TabularInline):
    """_summary_.

    Args:
        admin (_type_): _description_
    """

    model = GymCoach


# admins


@admin.register(Address)
class AddresAdmin(admin.ModelAdmin):
    """_summary_.

    Args:
        admin (_type_): _description_
    """

    model = Address


@admin.register(Coach)
class CoacheAdmin(admin.ModelAdmin):
    """_summary_.

    Args:
        admin (_type_): _description_
    """

    model = Coach
    form = CoachForm
    inlines = (GymCoachInline,)


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    """_summary_.

    Args:
        admin (_type_): _description_
    """

    model = Gym
    form = GymForm
    inlines = (GymCoachInline,)


@admin.register(Certificate)
class Certificate(admin.ModelAdmin):
    """_summary_.

    Args:
        admin (_type_): _description_
    """

    model = Certificate
    form = CertificateForm


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """_summary_.

    Args:
        admin (_type_): _description_
    """

    model = Subscription
