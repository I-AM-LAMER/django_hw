"""_summary_."""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import CharField, DecimalField, EmailField, Form, ModelForm

from .models import Certificate, Coach, Gym, Subscription

CHARFIELD_LENGTH = 100
MX_DIGITS = 11


class SubscriptionForm(ModelForm):
    """_summary_.

    Args:
        forms (_type_): _description_
    """

    class Meta:
        """_summary_."""

        model = Subscription
        exclude = ['id']


class GymForm(ModelForm):
    """_summary_.

    Args:
        forms (_type_): _description_
    """

    class Meta:
        """_summary_."""

        model = Gym
        exclude = ['id']


class CoachForm(ModelForm):
    """_summary_.

    Args:
        forms (_type_): _description_
    """

    class Meta:
        """_summary_."""

        model = Coach
        exclude = ['id']


class CertificateForm(ModelForm):
    """_summary_.

    Args:
        forms (_type_): _description_
    """

    class Meta:
        """_summary_."""

        model = Certificate
        exclude = ['id']


class RegistrationForm(UserCreationForm):
    """_summary_.

    Args:
        UserCreationForm (_type_): _description_
    """

    first_name = CharField(max_length=CHARFIELD_LENGTH, required=True)
    last_name = CharField(max_length=CHARFIELD_LENGTH, required=True)
    email = EmailField(max_length=CHARFIELD_LENGTH * 2, required=True)

    class Meta:
        """_summary_."""

        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class AddFundsForm(Form):
    """_summary_.

    Args:
        Form (_type_): _description_

    Returns:
        _type_: _description_
    """

    money = DecimalField(label='money', decimal_places=2, max_digits=MX_DIGITS)

    def is_valid(self) -> bool:
        """_summary_.

        Returns:
            bool: _description_
        """
        def add_error(error):
            """_summary_.

            Args:
                error (_type_): _description_
            """
            if self.errors:
                self.errors['money'] += [error]
            else:
                self.errors['money'] = [error]

        if not super().is_valid():
            return False
        money = self.cleaned_data.get('money', None)
        if not money:
            add_error(ValidationError('an error occured, money field was not specified!'))
            return False
        if money < 0:
            add_error(ValidationError('you can only add positive amount of money!'))
            return False
        return True
