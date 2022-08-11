from django.contrib import admin
from store.models import (
    Order,
    Promotion,
    UserInfo,
    Product,
    Category,
    ShoppingCart,
    OrderItem,
    ShoppingCartItem,
    Address,
)

admin.site.register(Order)
admin.site.register(Promotion)
admin.site.register(UserInfo)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ShoppingCart)
admin.site.register(OrderItem)
admin.site.register(ShoppingCartItem)
admin.site.register(Address)
