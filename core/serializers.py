from rest_framework import serializers

from core.models import Address, User, Product, OrderItem, Order, Payment


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


# Serializer para Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock']


# Serializer para OrderItem
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity']


# Serializer para Order
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = serializers.StringRelatedField(read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'created_at', 'updated_at', 'total_amount', 'status']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order


# Serializer para Payment
class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'timestamp', 'method', 'successful']