from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.serializers import CakeSerializer, UserSerializer
from core.models import Cake, User

from django.shortcuts import get_object_or_404
from django.contrib.auth import login


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
