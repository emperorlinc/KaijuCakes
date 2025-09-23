from django.contrib import admin

from core.models import Cart, Category, Cake, CartItem, Cart, User

# Register your models here.
admin.site.register(Category)
admin.site.register(Cake)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(User)
