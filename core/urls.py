from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.api_overview),
    path('register/', views.register),
    path('login/', views.login),
    path('access_token/', views.access_token),

    path('cakes/', views.cakes_list),
    path('cake/<int:pk>/', views.cake_detail),
    path('queryCakes/<str:query>/', views.query_cake),

    path('category/', views.category_list),
    path('category/<int:pk>/', views.category_detail),
]
