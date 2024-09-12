"""This module contains Django admin configurations for various models in the application."""

from django.contrib import admin

from .forms import CertificateForm, CoachForm, GymForm
from .models import Address, Certificate, Coach, Gym, GymCoach, Subscription


class GymCoachInline(admin.TabularInline):
    """
    Represents a tabular inline for editing GymCoach relationships.

    Attributes:
        model (model): The model associated with this inline.
    """

    model = GymCoach


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Address objects.

    Attributes:
        model (model): The model associated with this admin interface.
    """

    model = Address


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Coach objects.

    Attributes:
        model (model): The model associated with this admin interface.
        form (form): The custom form used for Coach objects.
        inlines (tuple): Inline models related to Coach.
    """

    model = Coach
    form = CoachForm
    inlines = (GymCoachInline,)


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Gym objects.

    Attributes:
        model (model): The model associated with this admin interface.
        form (form): The custom form used for Gym objects.
        inlines (tuple): Inline models related to Gym.
    """

    model = Gym
    form = GymForm
    inlines = (GymCoachInline,)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Certificate objects.

    Attributes:
        model (model): The model associated with this admin interface.
        form (form): The custom form used for Certificate objects.
    """

    model = Certificate
    form = CertificateForm


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Subscription objects.

    Attributes:
        model (model): The model associated with this admin interface.
    """

    model = Subscription
