"""_summary_."""

from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from .models import Certificate, Client, Coach, Gym, GymCoach, Subscription, Address, User

ALL = '__all__'


class ClientSerializer(ModelSerializer):
    """_summary_.

    Args:
        ModelSerializer (_type_): _description_

    Returns:
        _type_: _description_
    """

    class Meta:
        """_summary_."""

        model = Client
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """_summary_.

        Args:
            validated_data (_type_): _description_

        Returns:
            _type_: _description_
        """
        user = User.objects.create_user(**validated_data)
        client = Client.objects.create(user=user)
        Token.objects.create(user=user)
        return client


class GymSerializer(ModelSerializer):
    """_summary_.

    Args:
        ModelSerializer (_type_): _description_
    """

    coaches = PrimaryKeyRelatedField(many=True, queryset=Coach.objects.all())
    address = PrimaryKeyRelatedField(queryset=Address.objects.all())

    class Meta:
        """_summary_."""

        model = Gym
        fields = ['id', 'gym_name', 'address', 'coaches']
        read_only_fields=['id']


class SubscriptionSerializer(ModelSerializer):
    """_summary_.

    Args:
        ModelSerializer (_type_): _description_
    """
    
    gym = PrimaryKeyRelatedField(queryset=Gym.objects.all())
    clients = PrimaryKeyRelatedField(many=True, queryset=Client.objects.all())

    class Meta:
        """_summary_."""

        model = Subscription
        fields = ALL
        read_only_fields=['id']


class CoachSerializer(ModelSerializer):
    """_summary_.

    Args:
        ModelSerializer (_type_): _description_
    """

    gyms = PrimaryKeyRelatedField(many=True, queryset=Gym.objects.all())

    class Meta:
        """_summary_."""

        model = Coach
        fields = ['id', 'first_name', 'last_name', 'spec', 'gyms']
        read_only_fields=['id']


class CertificateSerializer(ModelSerializer):
    """_summary_.

    Args:
        ModelSerializer (_type_): _description_
    """

    coach = PrimaryKeyRelatedField(queryset=Coach.objects.all())

    class Meta:
        """_summary_."""

        model = Certificate
        fields = ['id', 'coach', 'certf_name', 'description']
        read_only_fields=['id']

class AddressSerializer(ModelSerializer):
    """_summary_.

    Args:
        ModelSerializer (_type_): _description_
    """

    class Meta:
        """_summary_."""

        model = Address
        fields = ALL
        read_only_fields=['id']
