from django.db import models
from django.contrib.auth.models import User


class Promotion(models.Model):
    description = models.TextField()
    discount = models.FloatField()

    def __str__(self):
        return f"{self.description[:20]}..."

    class Meta:
        ordering = ['description']


class UserInfo(models.Model):
    class Membership(models.TextChoices):
        BRONZE = 'B', 'Bronze'
        SILVER = 'S', 'Silver'
        GOLD = 'G', 'Gold'

    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(max_length=1, choices=Membership.choices, default=Membership.BRONZE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info', primary_key=True)

    def __str__(self):
        return self.user


class Address(models.Model):
    details = models.TextField()
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='addresses')

    class Meta:
        ordering = ['details']


class Category(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        to='Product', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='+'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.PositiveIntegerField(default=1)
    categories = models.ManyToManyField(Category, related_name='products', blank=True)
    promotions = models.ManyToManyField(Promotion, related_name='products', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title', 'created_at']


class ShoppingCart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']


class ShoppingCartItem(models.Model):
    quantity = models.PositiveSmallIntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='shopping_cart_items')
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.PROTECT, related_name='shopping_cart_items')


class Order(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'P', 'Pending'
        COMPLETE = 'C', 'Complete'
        FAILED = 'F', 'Failed'

    payment_status = models.CharField(max_length=1, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    customer = models.ForeignKey(UserInfo, on_delete=models.PROTECT, related_name='orders')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    quantity = models.PositiveSmallIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='order_items')
