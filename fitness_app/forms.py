"""
This module contains various forms used in the fitness application.

including subscription management, gym registration, coach registration,
certificate creation, and user registration.
"""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import CharField, DecimalField, EmailField, Form, ModelForm

from .models import Certificate, Coach, Gym, Subscription

CHARFIELD_LENGTH = 100
MX_DIGITS = 11


class SubscriptionForm(ModelForm):
    """
    Form for creating or updating Subscription objects.

    Attributes:
        model (model): The model associated with this form.
        exclude (tuple): Fields excluded from the form.
    """

    class Meta:
        """Meta class configuration for the SubscriptionForm."""

        model = Subscription
        exclude = ['id']


class GymForm(ModelForm):
    """
    Form for creating or updating Gym objects.

    Attributes:
        model (model): The model associated with this form.
        exclude (tuple): Fields excluded from the form.
    """

    class Meta:
        """Meta class configuration for the GymForm."""

        model = Gym
        exclude = ['id']


class CoachForm(ModelForm):
    """
    Form for creating or updating Coach objects.

    Attributes:
        model (model): The model associated with this form.
        exclude (tuple): Fields excluded from the form.
    """

    class Meta:
        """Meta class configuration for the CoachForm."""

        model = Coach
        exclude = ['id']


class CertificateForm(ModelForm):
    """
    Form for creating or updating Certificate objects.

    Attributes:
        model (model): The model associated with this form.
        exclude (tuple): Fields excluded from the form.
    """

    class Meta:
        """Meta class configuration for the CertificateForm."""

        model = Certificate
        exclude = ['id']


class RegistrationForm(UserCreationForm):
    """
    Custom UserCreationForm for user registration with additional fields.

    Attributes:
        first_name (CharField): First name field.
        last_name (CharField): Last name field.
        email (EmailField): Email address field.

    Returns:
        tuple: A tuple containing the cleaned data and None.
    """

    first_name = CharField(max_length=CHARFIELD_LENGTH, required=True)
    last_name = CharField(max_length=CHARFIELD_LENGTH, required=True)
    email = EmailField(max_length=CHARFIELD_LENGTH * 2, required=True)

    class Meta:
        """Meta class configuration for the RegistrationForm."""

        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class AddFundsForm(Form):
    """
    Form for adding funds to an account.

    Args:
        Form (_type_): Base Form class.

    Returns:
        bool: True if the form is valid, False otherwise.
    """

    money = DecimalField(label='money', decimal_places=2, max_digits=MX_DIGITS)

    def is_valid(self) -> bool:
        """
        Add custom validation method for the adding funds.

        Returns:
            bool: True if the form is valid, False otherwise.
        """
        def add_error(error):
            """
            Add Helper function to add errors to the form.

            Args:
                error (_type_): Error message to add.
            """
            if self.errors:
                self.errors['money'] += [error]
            else:
                self.errors['money'] = [error]

        if not super().is_valid():
            return False
        money = self.cleaned_data.get('money', None)
        if not money:
            add_error(ValidationError('an error occurred, money field was not specified!'))
            return False
        if money < 0:
            add_error(ValidationError('you can only add positive amount of money!'))
            return False
        return True
