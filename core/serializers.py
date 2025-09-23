from rest_framework import serializers
from core.models import Cake, Cart, CartItem, Category, User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        modes = Category
        fields = '__all__'


class CakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cake
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
