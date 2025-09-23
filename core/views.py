from unicodedata import category
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.serializers import CakeSerializer, CategorySerializer, UserSerializer
from core.models import Cake, Category, User

from django.shortcuts import get_object_or_404
from django.db.models import Q


# Create your views here.


@api_view(['GET'])
def api_overview(request):
    overview = [
        {
            'endpoint': 'register/',
            'function': 'Register a user.'
        }, {
            'endpoint': 'login/',
            'function': 'Login in a user.'
        }, {
            'endpoint': 'cakes/',
            'function': 'List of cakes.',
        }, {
            'endpoint': 'cake/<int:pk>/',
            'function': 'Cake details.',
        }, {
            'endpoint': 'category/',
            'function': 'List of categories of cakes.'
        }, {
            'endpoint': '<category name>/',
            'function': 'List of cakes in the category.'
        }, {
            'endpoint': 'cart/',
            'function': 'Cart'
        }, {
            'endpoint': 'order/',
            'function': 'Place order of the items in the cart.'
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
    serializers = CakeSerializer(cakes, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def cake_detail(request, pk):
    cakes = get_object_or_404(Cake, id=pk)
    serializers = CakeSerializer(cakes, many=False)
    return Response(serializers.data, status=status.HTTP_200_OK)


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
        return Response({"Detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_detail(request, pk):
    category = get_object_or_404(Category, id=pk)
    cakes = Cake.objects.filter(category=category)
    serializer = CategorySerializer(cakes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
