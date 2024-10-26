from django.contrib.auth.models import AbstractUser
from django.db import models

# Modelo de Endereço
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    commercial_address = models.OneToOneField(Address, null=True, blank=True, on_delete=models.SET_NULL, related_name='commercial_users')
    residential_address = models.OneToOneField(Address, null=True, blank=True, on_delete=models.SET_NULL, related_name='residential_users')

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    stock = models.IntegerField()


    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')  # Novo campo de status

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - Status: {self.status}"

# Item do Pedido para vincular produtos e quantidades no pedido
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('PIX', 'PIX'),
        ('Boleto', 'Boleto'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    successful = models.BooleanField(default=True)

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id} - Method: {self.method}"