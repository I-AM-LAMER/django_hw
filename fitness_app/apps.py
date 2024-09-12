"""This module contains the Django app configuration for the fitness application."""

from django.apps import AppConfig


class FitnessAppConfig(AppConfig):
    """
    Custom AppConfig for the fitness application.

    Attributes:
        default_auto_field (str): The default auto field type.
        name (str): The name of the app.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fitness_app'
