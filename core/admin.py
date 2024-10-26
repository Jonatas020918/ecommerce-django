from django.contrib import admin
from .models import User, Address, Product, Order, OrderItem, Payment

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)