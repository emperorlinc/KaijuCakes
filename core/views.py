from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# Create your views here.


@api_view(["GET"])
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
