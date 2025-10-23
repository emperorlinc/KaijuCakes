from rest_framework import serializers
from core.models import Cake, Cart, CartItem, Category, User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CakeSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta(object):
        model = Cake
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta(object):
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    cake = CakeSerializer()
    cart = CartSerializer()

    class Meta(object):
        model = CartItem
        fields = '__all__'
