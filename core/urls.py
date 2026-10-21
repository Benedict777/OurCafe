from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import MenuItemViewSet

router = DefaultRouter()
router.register('menu', MenuItemViewSet, basename='api-menu')

urlpatterns = [
    path('', views.home, name='home'),

    path('menu/', views.menu_list, name='menu_list'),
    path('menu/add/', views.menu_create, name='menu_create'),
    path('menu/<int:pk>/', views.menu_detail, name='menu_detail'),
    path('menu/<int:pk>/edit/', views.menu_update, name='menu_update'),
    path('menu/<int:pk>/delete/', views.menu_delete, name='menu_delete'),

    path('tables/', views.table_list, name='table_list'),
    path('tables/add/', views.table_create, name='table_create'),
    path('tables/<int:pk>/edit/', views.table_update, name='table_update'),
    path('tables/<int:pk>/delete/', views.table_delete, name='table_delete'),

    path('orders/', views.order_list, name='order_list'),
    path('orders/add/', views.order_create, name='order_create'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/edit/', views.order_update, name='order_update'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),

    path('register/', views.register, name='register'),

    path('api/', include(router.urls)),
]