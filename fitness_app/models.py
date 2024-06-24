"""summary."""

from uuid import uuid4

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

ADDRESS_NAME_LEN = 256
DESCRIPTION_MAX_LENGTH = 1024
MAX_AMOUNT_OF_MONEY = 10000000


def check_money(money: int | float) -> None:
    """_summary_.

    Args:
        money (int | float): _description_

    Raises:
        ValidationError: _description_
    """
    if money < 0 or money >= MAX_AMOUNT_OF_MONEY:
        raise ValidationError(('The money should be in the range between 0 and 9999999.99 inclusive!'),
            params={'money': money},
        )


def check_datetime(time) -> None:
    """_summary_.

    Args:
        time (_type_): _description_

    Raises:
        ValidationError: _description_
    """
    if time > timezone.now():
        raise ValidationError(
            message='Datetime is not valid',
            params={'created_datetime': time}
        )


def check_positive(number: int | float):
    """Check the number is positive.

    Args:
        number (int | float): your number

    Raises:
        ValidationError: Error for django admin
    """
    if number < 0:
        raise ValidationError(
            'number must be more than 0!',
            params={'number': number},
            )


def check_body(body: str):
    """Check body`s stucture.

    Args:
        body (str): your body

    Raises:
        ValidationError: django error
    """
    if not body.isdigit() and len(body) > 1:
        raise ValidationError(
            'Body can only contain one letter',
            params={'body': body},
        )
    if body.isdigit():
        check_positive(int(body))


def check_address_len(address: str):
    """_summary_.

    Args:
        address (str): _description_

    Raises:
        ValidationError: _description_
    """
    if len(address) <= 10:
        raise ValidationError('address length cannot be less than 10!')


def check_date(date):
    """_summary_.

    Args:
        date (_type_): _description_

    Raises:
        ValidationError: _description_
    """
    if date < timezone.localdate():
        raise ValidationError(f'date is not valid')


class CreatedMixin(models.Model):
    """_summary_.

    Args:
        models (_type_): _description_
    """

    created_datetime = models.DateTimeField(
        null=True, blank=True,
        default=timezone.now, 
        validators=[
            check_datetime,
        ]
    )

    class Meta:
        """_summary_."""

        abstract = True


class ModifiedMixin(models.Model):
    """_summary_.

    Args:
        models (_type_): _description_
    """

    modified_datetime = models.DateTimeField(
        null=True, blank=True,
        default=timezone.now, 
        validators=[
            check_datetime,
        ]
    )

    class Meta:
        """_summary_."""

        abstract = True


class UUIDMixin(models.Model):
    """_summary_.

    Args:
        models (_type_): _description_
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    class Meta:
        """_summary_."""

        abstract = True


class Address(UUIDMixin, CreatedMixin, ModifiedMixin):
    """_summary_.

    Args:
        UUIDMixin (_type_): _description_
        CreatedMixin (_type_): _description_
        ModifiedMixin (_type_): _description_

    Returns:
        _type_: _description_
    """

    city_name = models.TextField(max_length=ADDRESS_NAME_LEN, null=False, blank=False)
    street_name = models.TextField(max_length=ADDRESS_NAME_LEN, null=False, blank=False)
    house_number = models.IntegerField(null=False, blank=False, validators=[check_positive])
    apartment_number = models.IntegerField(null=True, blank=True, validators=[check_positive])
    body = models.TextField(null=True, blank=True, validators=[check_body])

    def __str__(self) -> str:
        return f'{self.city_name}/{self.street_name}/{self.house_number}'
    
    class Meta:
        """_summary_."""

        db_table = '"address"'
        verbose_name = "address"


class Gym(UUIDMixin, CreatedMixin, ModifiedMixin):
    """_summary_.

    Args:
        UUIDMixin (_type_): _description_
        CreatedMixin (_type_): _description_
        ModifiedMixin (_type_): _description_

    Returns:
        _type_: _description_
    """

    gym_name = models.CharField(max_length=100, null=False, blank=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    coaches = models.ManyToManyField('Coach', through='GymCoach')

    def __str__(self) -> str:
        return f'{self.gym_name}'

    class Meta:
        """_summary_."""

        db_table = '"gym"'
        verbose_name = "gym"


class Coach(UUIDMixin, CreatedMixin, ModifiedMixin):
    """_summary_.

    Args:
        UUIDMixin (_type_): _description_
        CreatedMixin (_type_): _description_
        ModifiedMixin (_type_): _description_
    """

    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    spec = models.CharField(max_length=100, null=False, blank=False)

    gyms = models.ManyToManyField('Gym', through='GymCoach')

    class Meta:
        db_table = '"coach"'
        verbose_name = "coach"


class Certificate(UUIDMixin, CreatedMixin, ModifiedMixin):
    """_summary_.

    Args:
        UUIDMixin (_type_): _description_
        CreatedMixin (_type_): _description_
        ModifiedMixin (_type_): _description_
    """

    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    certf_name = models.CharField(max_length=50, null=False, blank=False),
    description = models.TextField(max_length=1000, blank=True)

    class Meta:
        """_summary_."""

        db_table = '"certf"'


class GymCoach(UUIDMixin):
    """_summary_.

    Args:
        UUIDMixin (_type_): _description_
    """

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)

    class Meta:
        """_summary_."""

        db_table = '"gym_coach"'
        unique_together = (('gym', 'coach'))


class Client(UUIDMixin):
    """_summary_.

    Args:
        UUIDMixin (_type_): _description_

    Returns:
        _type_: _description_
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    net_worth = models.DecimalField(null=False, blank=False, max_digits=9, decimal_places=2, validators=[check_money,], default=1000)

    subs = models.ManyToManyField('Subscription', through='ClientSub')

    def __str__(self) -> str:
        return f'{self.user.username} ({self.user.first_name} {self.user.last_name})'
    
    def save(self, *args, **kwargs):
        check_money(self.net_worth)
        super().save(*args, **kwargs)
    
    class Meta:
        """_summary_."""

        db_table = '"client"'


class Subscription(UUIDMixin, CreatedMixin, ModifiedMixin):
    """_summary_.

    Args:
        UUIDMixin (_type_): _description_
        CreatedMixin (_type_): _description_
        ModifiedMixin (_type_): _description_
    """

    price = models.IntegerField(null=False, blank=False)
    expire_date = models.DateField(null=False, blank=False, validators=[check_date])
    description = models.TextField(null=True, blank=True, max_length=DESCRIPTION_MAX_LENGTH)

    gym = models.ForeignKey(Gym, blank=False, null=False, on_delete=models.CASCADE)
    clients = models.ManyToManyField('Client', through='ClientSub')

    class Meta:
        """_summary_."""

        db_table = '"subscription"'


class ClientSub(UUIDMixin):
    """_summary_.

    Args:
        UUIDMixin (_type_): _description_
    """

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sub = models.ForeignKey(Subscription, on_delete=models.CASCADE)

    class Meta:
        """_summary_."""

        db_table = '"client_sub"'
        unique_together = (('sub', 'client'))
