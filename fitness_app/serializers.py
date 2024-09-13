"""_summary_."""

from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from .models import (Address, Certificate, Client, Coach, Gym, Subscription,
                     User)

ALL = '__all__'


class ClientSerializer(ModelSerializer):
    """Client serializer.

    Args:
        ModelSerializer (_type_): Base serializer class.

    Returns:
        _type_: Serialized client data.

    Attributes:
        username (str): Username of the client.
        email (str): Email address of the client.
        password (str): Password for the client account.
    """

    class Meta:
        """Meta options for ClientSerializer.

        Attributes:
            model (Client): The model associated with this serializer.
            fields (tuple): Fields to be included in the serialization.
            extra_kwargs (dict): Extra keyword arguments for fields.
        """

        model = Client
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create a new client instance.

        Args:
            validated_data (dict): Validated data for creating a client.

        Returns:
            Client: Created client instance.
        """
        user = User.objects.create_user(**validated_data)
        client = Client.objects.create(user=user)
        Token.objects.create(user=user)
        return client


class GymSerializer(ModelSerializer):
    """Gym serializer.

    Args:
        ModelSerializer (_type_): Base serializer class.

    Returns:
        _type_: Serialized gym data.

    Attributes:
        id (int): Unique identifier for the gym.
        gym_name (str): Name of the gym.
        address (int): Primary key of the associated address.
        coaches (list[int]): List of primary keys of associated coaches.
        image_path (str): Path to the gym's image.
    """

    coaches = PrimaryKeyRelatedField(many=True, queryset=Coach.objects.all())
    address = PrimaryKeyRelatedField(queryset=Address.objects.all())

    class Meta:
        """Meta options for GymSerializer.

        Attributes:
            model (Gym): The model associated with this serializer.
            fields (list): Fields to be included in the serialization.
            read_only_fields (list): Fields that are read-only.
        """

        model = Gym
        fields = ['id', 'gym_name', 'address', 'coaches']
        read_only_fields = ['id']


class SubscriptionSerializer(ModelSerializer):
    """Subscription serializer.

    Args:
        ModelSerializer (_type_): Base serializer class.

    Returns:
        _type_: Serialized subscription data.

    Attributes:
        id (int): Unique identifier for the subscription.
        gym (int): Primary key of the associated gym.
        clients (list[int]): List of primary keys of associated clients.
    """

    gym = PrimaryKeyRelatedField(queryset=Gym.objects.all())
    clients = PrimaryKeyRelatedField(many=True, queryset=Client.objects.all())

    class Meta:
        """Meta options for SubscriptionSerializer.

        Attributes:
            model (Subscription): The model associated with this serializer.
            fields (str): Fields to be included in the serialization.
            read_only_fields (list): Fields that are read-only.
        """

        model = Subscription
        fields = ALL
        read_only_fields = ['id']


class CoachSerializer(ModelSerializer):
    """Coach serializer.

    Args:
        ModelSerializer (_type_): Base serializer class.

    Returns:
        _type_: Serialized coach data.

    Attributes:
        id (int): Unique identifier for the coach.
        first_name (str): First name of the coach.
        last_name (str): Last name of the coach.
        spec (str): Specialization of the coach.
        gyms (list[int]): List of primary keys of associated gyms.
        image_path (str): Path to the coach's image.
    """

    gyms = PrimaryKeyRelatedField(many=True, queryset=Gym.objects.all())

    class Meta:
        """Meta options for CoachSerializer.

        Attributes:
            model (Coach): The model associated with this serializer.
            fields (list): Fields to be included in the serialization.
            read_only_fields (list): Fields that are read-only.
        """

        model = Coach
        fields = ['id', 'first_name', 'last_name', 'spec', 'gyms']
        read_only_fields = ['id']


class CertificateSerializer(ModelSerializer):
    """Certificate serializer.

    Args:
        ModelSerializer (_type_): Base serializer class.

    Returns:
        _type_: Serialized certificate data.

    Attributes:
        id (int): Unique identifier for the certificate.
        coach (int): Primary key of the associated coach.
        certf_name (str): Name of the certificate.
        description (str): Description of the certificate.
    """

    coach = PrimaryKeyRelatedField(queryset=Coach.objects.all())

    class Meta:
        """Meta options for CertificateSerializer.

        Attributes:
            model (Certificate): The model associated with this serializer.
            fields (list): Fields to be included in the serialization.
            read_only_fields (list): Fields that are read-only.
        """

        model = Certificate
        fields = ['id', 'coach', 'certf_name', 'description']
        read_only_fields = ['id']


class AddressSerializer(ModelSerializer):
    """Address serializer.

    Args:
        ModelSerializer (_type_): Base serializer class.

    Returns:
        _type_: Serialized address data.

    Attributes:
        id (int): Unique identifier for the address.
        street (str): Street name.
        house_number (str): House number.
        city (str): City name.
        zip_code (str): ZIP code.
    """

    class Meta:
        """Meta options for AddressSerializer.

        Attributes:
            model (Address): The model associated with this serializer.
            fields (str): Fields to be included in the serialization.
            read_only_fields (list): Fields that are read-only.
        """

        model = Address
        fields = ALL
        read_only_fields = ['id']
