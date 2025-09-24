from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.api_overview),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('access_token/', views.access_token),

    path('cakes/', views.cakes_list),
    path('cake_create/', views.cake_create),
    path('cake/<int:pk>/', views.cake_detail),
    path('cake_update/<int:pk>/', views.cake_update),
    path('cake_delete/<int:pk>/', views.cake_delete),
    path('queryCakes/<str:query>/', views.query_cake),

    path('category/', views.category_list),
    path('category_create/', views.category_create),
    path('category/<int:pk>/', views.category_detail),
    path('category_delete/<int:pk>/', views.category_delete),

    path('cart/', views.cart),
    path('add_to_cart/<int:pk>/', views.add_to_cart),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart),
    path('remove_cart_item/<int:pk>/', views.remove_cart_item),
]
