"""_summary_."""

from rest_framework.authtoken.models import Token
from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Certificate, Client, Coach, Gym, GymCoach, Subscription

ALL = '__all__'


class ClientSerializer(HyperlinkedModelSerializer):
    """_summary_.

    Args:
        HyperlinkedModelSerializer (_type_): _description_

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
        user = Client.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class GymSerializer(HyperlinkedModelSerializer):
    """_summary_.

    Args:
        HyperlinkedModelSerializer (_type_): _description_
    """

    class Meta:
        """_summary_."""

        model = Gym
        fields = ALL


class SubscriptionSerializer(HyperlinkedModelSerializer):
    """_summary_.

    Args:
        HyperlinkedModelSerializer (_type_): _description_
    """

    class Meta:
        """_summary_."""

        model = Subscription
        fields = ALL


class CoachSerializer(HyperlinkedModelSerializer):
    """_summary_.

    Args:
        HyperlinkedModelSerializer (_type_): _description_
    """

    class Meta:
        """_summary_."""

        model = Coach
        fields = ALL


class CertificateSerializer(HyperlinkedModelSerializer):
    """_summary_.

    Args:
        HyperlinkedModelSerializer (_type_): _description_
    """

    class Meta:
        """_summary_."""

        model = Certificate
        fields = ALL


class GymCoachSerializer(HyperlinkedModelSerializer):
    """_summary_.

    Args:
        HyperlinkedModelSerializer (_type_): _description_
    """

    class Meta:
        """_summary_."""

        model = GymCoach
        fields = ALL
