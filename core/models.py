from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, username, password=None):
        if not email:
            raise ValueError('Email address is required.')
        user = self.normalize_email(email)
        user = self.model(email=email, name=name, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, username, password):
        user = self.create_user(email, name, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(models.Model):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=64, unique=True)
    name = models.CharField(max_length=64)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name


class Cake(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    step = models.IntegerField(default=1)

    def __str__(self) -> str:
        return self.name


class CartItem(models.Model):
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digit=6, decimal_places=2)

    def __str__(self) -> str:
        return self.cake.name

    @property
    def total_price(self):
        return self.cake.price * self.quantity


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart_item = models.ForeignKey(
        CartItem, on_delete=models.CASCADE, blank=True, null=True)
    total_cart_price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self) -> str:
        return self.item.cake.name


# TODO: ORDER TABLE.
