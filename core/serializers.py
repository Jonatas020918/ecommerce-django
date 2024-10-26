from rest_framework import serializers

from core.models import Address, User


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'state', 'postal_code', 'country']

class UserSerializer(serializers.ModelSerializer):
    residential_address = AddressSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'residential_address', 'commercial_address']


class UserRegistrationSerializer(serializers.ModelSerializer):
    residential_address = AddressSerializer()
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password', 'residential_address', 'commercial_address']
        extra_kwargs = {'commercial_address': {'required': False}, 'phone': {'required': False}}

    def create(self, validated_data):
        residential_address_data = validated_data.pop('residential_address')
        residential_address = Address.objects.create(**residential_address_data)

        password = validated_data.pop('password')

        user = User.objects.create(
            residential_address=residential_address,
            **validated_data
        )
        user.set_password(password)
        user.save()

        return user