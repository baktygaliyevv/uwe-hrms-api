"""
URL configuration for hrmsAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from .methods.users.views import UserListCreateAPIView, EditDeleteUser
from .methods.menu.views import GetMenuItems, AddMenuItem, EditMenuItem, DeleteMenuItem, AddMenuCategory, AddMenuProduct, DeleteMenuProduct, GetMenuCategories
from .methods.products.views import GetProducts, AddProduct, DeleteProduct, EditProduct
from .methods.promocodes.views import GetAllPromocodes, AddPromocode, DeletePromocode, GetSpecificPromocode
from .methods.tables.views import EditDeleteTable, GetAllTables, AddTable
from .methods.orders.views import GetAddOrder, GetAddClientOrder, EditDeleteOrder, AddOrderMenu, EditDeleteOrderMenu
from .methods.restaurants.views import GetRestaurant,DeleteRestaurant
from .methods.auth.views import AuthView, AuthLoginView, AuthSignupView, AuthVerifyView
from .methods.delivery.views import GetDeliveries, AddDelivery, EditDelivery, DeleteDelivery, AddUiClientDelivery

# FIXME that's not ok :(
API_BASE_URL = 'api/v1/'

urlpatterns = [
    #users
    path(f'{API_BASE_URL}users', UserListCreateAPIView.as_view(), name='get-users'),
    path(f'{API_BASE_URL}users/<int:id>', EditDeleteUser.as_view(), name='edit-user'),

    #menu
    path(f'{API_BASE_URL}menu', GetMenuItems.as_view(), name='get-menu-item'),
    path(f'{API_BASE_URL}menu', AddMenuItem.as_view(), name='add-menu-item'),
    path(f'{API_BASE_URL}menu/<int:id>', EditMenuItem.as_view(), name='edit-menu-item'),
    path(f'{API_BASE_URL}menu/<int:id>', DeleteMenuItem.as_view(), name='delete-menu-item'),
    path(f'{API_BASE_URL}menu/<int:id>/products', AddMenuProduct.as_view(), name='add-menu-product'),
    path(f'{API_BASE_URL}menu/<int:id>/products/<int:productId>', DeleteMenuProduct.as_view(), name='delete-menu-product'),
    path(f'{API_BASE_URL}menu/categories', GetMenuCategories.as_view(), name='get-menu-categories'),
    path(f'{API_BASE_URL}menu/categories', AddMenuCategory.as_view(), name='add-menu-category'),

    #products
    path(f'{API_BASE_URL}products', GetProducts.as_view(), name='get-products'),
    path(f'{API_BASE_URL}products', AddProduct.as_view(), name='add-product'),
    path(f'{API_BASE_URL}products/<int:id>', EditProduct.as_view(), name='edit-product'),
    path(f'{API_BASE_URL}products/<int:id>', DeleteProduct.as_view(), name='delete-product'),

    #promocodes
    path(f'{API_BASE_URL}promocodes', GetAllPromocodes.as_view(), name='get-promocodes'),
    path(f'{API_BASE_URL}promocodes', AddPromocode.as_view(), name='add-promocode'),
    path(f'{API_BASE_URL}promocodes/<id>', DeletePromocode.as_view(), name='delete-promocode'),
    path(f'{API_BASE_URL}promocodes/<id>', GetSpecificPromocode.as_view(), name='get-specific-promocode'),

    #tables
    path(f'{API_BASE_URL}tables', GetAllTables.as_view(), name='get-tables'),
    path(f'{API_BASE_URL}tables', AddTable.as_view(), name='add-tables'),
    path(f'{API_BASE_URL}tables/<int:id>', EditDeleteTable.as_view(), name='edit-delete-table'),

    #auth
    path(f'{API_BASE_URL}auth', AuthView.as_view(), name='auth'),
    path(f'{API_BASE_URL}auth/login', AuthLoginView.as_view(), name='auth-login'),
    path(f'{API_BASE_URL}auth/signup', AuthSignupView.as_view(), name='auth-signup'),
    path(f'{API_BASE_URL}auth/verify', AuthVerifyView.as_view(), name='auth-verify'),

    #orders
    path(f'{API_BASE_URL}orders', GetAddOrder.as_view(),name='get-add-orders'),
    path(f'{API_BASE_URL}orders/client', GetAddClientOrder.as_view(),name='get-add-client-order'),
    path(f'{API_BASE_URL}orders/<int:id>', EditDeleteOrder.as_view(),name='edit-delete-order'),
    path(f'{API_BASE_URL}orders/<int:order_id>/items', AddOrderMenu.as_view(),name='add-order-menu-items'),
    path(f'{API_BASE_URL}orders/<int:order_id>/items/<int:menu_id>',EditDeleteOrderMenu.as_view(),name='edit-delete-order-menu-item'),

    #restaurants
    path(f'{API_BASE_URL}restaurants', GetRestaurant.as_view(),name='get-restaurants'),
    path(f'{API_BASE_URL}restaurants/<int:id>',DeleteRestaurant.as_view(),name='delete-restaurant'),

    #deliveries
    path(f'{API_BASE_URL}deliveries',GetDeliveries.as_view(),name='get-delivery'),
    path(f'{API_BASE_URL}deliveries', AddDelivery.as_view(),name='add-delivery'),
    path(f'{API_BASE_URL}deliveries/client', AddUiClientDelivery.as_view(),name='add-ui-delivery'),
    path(f'{API_BASE_URL}deliveries/<int:id>', EditDelivery.as_view(), name='edit-delivery'),
    path(f'{API_BASE_URL}deliveries/<int:id>', DeleteDelivery.as_view(), name='delete-delivery'),

]
