from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.serializers import CakeSerializer, CartItemSerializer, CartSerializer, CategorySerializer, UserSerializer
from core.models import Cake, Cart, CartItem, Category, User
from core.permissions import IsSuperuserOrReadOnly, IsHostOrReadOnly

from django.shortcuts import get_object_or_404
from django.db.models import Q


# Create your views here.


@api_view(['GET'])
def api_overview(request):
    overview = [
        {
            'endpoint': 'register/',
            'function': 'Register a user.',
            'method': 'post'
        }, {
            'endpoint': 'login/',
            'function': 'Login in a user.',
            'method': 'post'
        }, {
            'endpoint': 'access_token/',
            'function': 'Use the access token to get the user detail.',
            'method': 'get'
        }, {
            'endpoint': 'cakes/',
            'function': 'List of cakes.',
            'method': 'get'
        }, {
            'endpoint': 'cake/<int:pk>/',
            'function': 'Cake details.',
            'method': 'get'
        }, {
            'endpoint': 'cake_create/',
            'function': 'Create cake.',
            'method': 'post',
            'restriction': 'Only a superuser can create a cake.'
        }, {
            'endpoint': 'cake_update/<int:pk>/',
            'function': 'Update cake.',
            'method': 'patch',
            'restriction': 'Only a superuser can update a cake'
        }, {
            'endpoint': 'cake_delete/<int:pk>/',
            'function': 'Delete cake.',
            'method': 'delete',
            'restriction': 'Only a superuser can delete a cake.'
        },  {
            'endpoint': 'queryCakes/<str:query>/',
            'function': 'Query cake by name or color.',
            'method': 'get'
        }, {
            'endpoint': 'category/',
            'function': 'List of categories of cakes.',
            'method': 'get'
        }, {
            'endpoint': 'category_create/',
            'function': 'Create cake category.',
            'method': 'create',
            'restriction': 'Only a superuser can create a category.'
        }, {
            'endpoint': 'category_delete/<int:pk>/',
            'function': 'Delete a cake category.',
            'method': 'delete',
            'restriction': 'Only a superuser can delete a category.'
        }, {
            'endpoint': 'category/<int:pk>/',
            'function': 'List of cakes in the category.',
            'method': 'get'
        }, {
            'endpoint': 'add_to_cart/<int:pk>/',
            'function': 'Add items to cart.',
            'method': 'post'
        }, {
            'endpoint': 'remove_from_cart/<int:pk>/',
            'function': 'Remove items from cart.',
            'method': 'post'
        }, {
            'endpoint': 'cart/',
            'function': 'Get cart.',
            'method': 'get'
        }
    ]
    return Response(overview, status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({
            "token": token.key,
            "user": serializer.data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({"message": "Not found."}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def access_token(request):

    serializer = UserSerializer(instance=request.user)
    return Response({"user": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def cakes_list(request):
    cakes = Cake.objects.all()
    serializer = CakeSerializer(cakes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsSuperuserOrReadOnly])
def cake_create(request):
    cake = CakeSerializer(data=request.data)
    if cake.is_valid():
        if request.user.is_superuser:
            cake.save()
    serializer = CakeSerializer(cake, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsSuperuserOrReadOnly])
def cake_update(request, pk):

    cake = get_object_or_404(Cake, id=pk)

    serializer = CakeSerializer(instance=cake, data=request.data)
    if cake.is_valid():
        cake.save()
    serializer = CakeSerializer(cake, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsSuperuserOrReadOnly])
def cake_delete(request, pk):
    cake = get_object_or_404(cake, id=pk)
    if request.user.is_superuser:
        cake.delete()
    return Response({"message": "Deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def cake_detail(request, pk):
    cake = get_object_or_404(Cake, id=pk)
    serializer = CakeSerializer(cake, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def query_cake(request, query):
    if query:
        cakes = Cake.objects.filter(
            Q(name__icontains=query) |
            Q(color__icontains=query)
        )
    else:
        cakes = Cake.objects.all()
    serializers = CakeSerializer(cakes, many=True)
    return Response(serializers.data, status=status.HTTP_302_FOUND)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_list(request):
    try:
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
    except:
        return Response({"message": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsSuperuserOrReadOnly])
def category_create(request):
    category = CategorySerializer(data=request.data)
    if category.is_valid():
        if request.user.is_superuser:
            category.save()
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_detail(request, pk):
    category = get_object_or_404(Category, id=pk)
    cakes = Cake.objects.filter(category=category)
    serializer = CategorySerializer(cakes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsSuperuserOrReadOnly])
def category_delete(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.user.is_superuser:
        category.delete()
    return Response({"message": "Deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsHostOrReadOnly])
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    if not created:
        cart_item = CartItem.objects.filter(cart=cart)
    serializer = CartItemSerializer(cart_item, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsHostOrReadOnly])
def add_to_cart(request, pk):
    cart = get_object_or_404(Cart,  user=request.user)
    cake = get_object_or_404(Cake, id=pk)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, cake=cake)

    if created:
        cart_item.total_price = cart_item.total_price()
    else:
        cart_item.quantity += 1
        cart_item.total_price = cart_item.total_price()

    cart_item.save()
    serializer = CartItemSerializer(instance=cart_item)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsHostOrReadOnly])
def remove_from_cart(request, pk):
    cart = get_object_or_404(Cart, user=request.user)
    cake = get_object_or_404(Cake, id=pk)

    try:
        cart_item = CartItem.objects.get(cart=cart, cake=cake)
    except:
        return Response({"message": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if cart_item.quantity <= 0:
        cart_item.delete()
    else:
        cart_item.quantity -= 1
        cart_item.total_price = cart_item.total_price
        cart_item.save()

    serializer = CartItemSerializer(instance=cart_item)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsHostOrReadOnly])
def remove_cart_item(request, pk):
    cart = get_object_or_404(Cart, user=request.user)
    cake = get_object_or_404(Cake, id=pk)

    try:
        cart_item = CartItem.objects.get(cart=cart, cake=cake)
    except:
        return Response({"message": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    cart_item.delete()

    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)
