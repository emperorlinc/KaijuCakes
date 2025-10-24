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


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=64, unique=True)
    name = models.CharField(max_length=64)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username']

    objects = CustomUserManager()

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
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    step = models.IntegerField(default=1)
    color = models.CharField(max_length=64, null=True)
    image = models.ImageField(upload_to='img', blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class CartItem(models.Model):
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    item_total_price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)

    def __str__(self) -> str:
        return self.cake.name

    def total_price(self):
        return self.cake.price * self.quantity


class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user')
    cart_item = models.ManyToManyField(CartItem)
    total_cart_price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)

    def __str__(self) -> str:
        return self.user.username
