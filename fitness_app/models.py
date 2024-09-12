"""
This module defines various utility functions and Django models for managing.

addresses, gyms, coaches, certificates, and subscriptions.
"""

from uuid import uuid4

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

ADDRESS_NAME_LEN = 256
DESCRIPTION_MAX_LENGTH = 1024
MAX_AMOUNT_OF_MONEY = 10000000
MAX_NAME_LENGTH = 50


def check_money(money: int | float) -> None:
    """
    Validate the amount of money.

    Args:
        money (int | float): The amount of money to validate.

    Raises:
        ValidationError: If the money is negative or exceeds the maximum allowed amount.
    """
    if money < 0 or money >= MAX_AMOUNT_OF_MONEY:
        raise ValidationError(
            (
                'The money should be in the range between 0 and 9999999.99 inclusive!'
            ),
            params={'money': money},
        )


def check_datetime(time) -> None:
    """
    Check if the given datetime is valid.

    Args:
        time: The datetime to check.

    Raises:
        ValidationError: If the datetime is in the future.
    """
    if time > timezone.now():
        raise ValidationError(
            message='Datetime is not valid',
            params={'created_datetime': time},
        )


def check_positive(number: int | float):
    """
    Check if the number is positive.

    Args:
        number (int | float): The number to check.

    Raises:
        ValidationError: If the number is not positive.
    """
    if number < 0:
        raise ValidationError(
            'number must be more than 0!',
            params={'number': number},
        )


def check_body(body: str):
    """
    Check the structure of the body.

    Args:
        body (str): The body to check.

    Raises:
        ValidationError: If the body contains more than one character or is numeric.
    """
    if not body.isdigit() and len(body) > 1:
        raise ValidationError(
            'Body can only contain one letter',
            params={'body': body},
        )
    if body.isdigit():
        check_positive(int(body))


def check_address_len(address: str):
    """
    Check the length of the address.

    Args:
        address (str): The address to check.

    Raises:
        ValidationError: If the address is shorter than 10 characters.
    """
    if len(address) <= 10:
        raise ValidationError('address length cannot be less than 10!')


def check_date(date):
    """
    Check if the date is valid.

    Args:
        date: The date to check.

    Raises:
        ValidationError: If the date is in the past.
    """
    if date < timezone.localdate():
        raise ValidationError('date is not valid')


class CreatedMixin(models.Model):
    """Mixin for automatically setting created datetime."""

    created_datetime = models.DateTimeField(
        null=True,
        blank=True,
        default=timezone.now,
        validators=[
            check_datetime,
        ],
    )

    class Meta:
        """Metadata for CreatedMixin."""

        abstract = True


class ModifiedMixin(models.Model):
    """Mixin for automatically setting modified datetime."""

    modified_datetime = models.DateTimeField(
        null=True,
        blank=True,
        default=timezone.now,
        validators=[
            check_datetime,
        ],
    )

    class Meta:
        """Metadata for ModifiedMixin."""

        abstract = True


class UUIDMixin(models.Model):
    """Mixin for using UUID as primary key."""

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    class Meta:
        """Metadata for UUIDMixin."""

        abstract = True


class Address(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model representing an address."""

    city_name = models.TextField(max_length=ADDRESS_NAME_LEN, null=False, blank=False)
    street_name = models.TextField(max_length=ADDRESS_NAME_LEN, null=False, blank=False)
    house_number = models.IntegerField(null=False, blank=False, validators=[check_positive])
    apartment_number = models.IntegerField(null=True, blank=True, validators=[check_positive])
    body = models.TextField(null=True, blank=True, validators=[check_body])

    def __str__(self) -> str:
        """Represent Address class.

        Returns:
            str: string representation
        """
        return f'{self.city_name}/{self.street_name}/{self.house_number}'

    class Meta:
        """Metadata for Address model."""

        db_table = '"address"'
        verbose_name = "address"


class Gym(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model representing a gym."""

    gym_name = models.CharField(max_length=100, null=False, blank=False)
    address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.CASCADE)
    coaches = models.ManyToManyField('Coach', through='GymCoach')

    def __str__(self) -> str:
        """Represent Gym class.

        Returns:
            str: gym name
        """
        return f'{self.gym_name}'

    class Meta:
        """Metadata for Gym model."""

        db_table = '"gym"'
        verbose_name = "gym"


class Coach(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model representing a coach."""

    first_name = models.CharField(max_length=MAX_NAME_LENGTH, null=False, blank=False)
    last_name = models.CharField(max_length=MAX_NAME_LENGTH, null=False, blank=False)
    spec = models.CharField(max_length=100, null=False, blank=False)

    gyms = models.ManyToManyField('Gym', through='GymCoach')

    class Meta:
        """Metadata for Coach model."""

        db_table = '"coach"'
        verbose_name = "coach"


class Certificate(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model representing a certificate."""

    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    certf_name = models.CharField(max_length=MAX_NAME_LENGTH, null=False, blank=False)
    description = models.TextField(max_length=1000, blank=True)

    class Meta:
        """Metadata for Certificate model."""

        db_table = '"certf"'


class GymCoach(UUIDMixin):
    """Model representing a gym-coach relationship."""

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)

    class Meta:
        """Metadata for GymCoach model."""

        db_table = '"gym_coach"'
        unique_together = (('gym', 'coach'))


class Client(UUIDMixin):
    """Model representing a client."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    net_worth = models.DecimalField(
        null=False,
        blank=False,
        max_digits=9,
        decimal_places=2,
        validators=[check_money],
        default=1000,
        )

    subs = models.ManyToManyField('Subscription', through='ClientSub')

    def __str__(self) -> str:
        """Represent Client class.

        Returns:
            str: user creditionals
        """
        return '{0} ({1} {2})'.format(self.user.username, self.user.first_name, self.user.last_name)

    def save(self, *args, **kwargs):
        """Save."""
        check_money(self.net_worth)
        super().save(*args, **kwargs)

    class Meta:
        """Metadata for Client model."""

        db_table = '"client"'


class Subscription(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model representing a subscription."""

    price = models.IntegerField(null=False, blank=False, validators=[check_money])
    expire_date = models.DateField(null=False, blank=False, validators=[check_date])
    description = models.TextField(null=True, blank=True, max_length=DESCRIPTION_MAX_LENGTH)

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    clients = models.ManyToManyField('Client', through='ClientSub')

    class Meta:
        """Metadata for Subscription model."""

        db_table = '"subscription"'


class ClientSub(UUIDMixin):
    """Model representing a client-subscription relationship."""

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sub = models.ForeignKey(Subscription, on_delete=models.CASCADE)

    class Meta:
        """Metadata for ClientSub model."""

        db_table = '"client_sub"'
        unique_together = (('sub', 'client'))
