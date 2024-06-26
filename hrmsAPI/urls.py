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
from .methods.menu.views import GetAddMenuItems, EditDeleteMenuItem, AddMenuProduct, DeleteMenuProduct, GetAddMenuCategories, available_menu_items, unavailable_menu_items
from .methods.products.views import GetAddProducts, EditDeleteProduct
from .methods.promocodes.views import GetAddPromocodes, GetDeleteSpecificPromocode
from .methods.tables.views import EditDeleteTable, GetAddTables
from .methods.orders.views import GetAddOrder, GetAddClientOrder, EditDeleteOrder, AddOrderMenu, EditDeleteOrderMenu
from .methods.restaurants.views import GetRestaurant,DeleteRestaurant
from .methods.auth.views import AuthView, AuthLoginView, AuthSignupView, AuthVerifyView
from .methods.delivery.views import GetAddDelivery, EditDeleteDelivery, GetAddClientDeliveries, AddDeliveryMenu,EditDeleteDeliveryMenu
from .methods.storage.views import GetRetaurantProducts, IncRestaurntProducts, DecRestaurntProducts
from .methods.bookings.views import GetAddBookings, EditDeleteBooking, ClientGetAddBookings

# FIXME that's not ok :(
API_BASE_URL = 'api/v1/'

urlpatterns = [
    #users
    path(f'{API_BASE_URL}users', UserListCreateAPIView.as_view(), name='get-add-users'),
    path(f'{API_BASE_URL}users/<int:id>', EditDeleteUser.as_view(), name='edit-delete-user'),

    #menu
    path(f'{API_BASE_URL}menu', GetAddMenuItems.as_view(), name='get-add-menu-item'),
    path(f'{API_BASE_URL}menu/<int:id>', EditDeleteMenuItem.as_view(), name='edit-delete-menu-item'),
    path(f'{API_BASE_URL}menu/<int:id>/products', AddMenuProduct.as_view(), name='add-menu-product'),
    path(f'{API_BASE_URL}menu/<int:id>/products/<int:productId>', DeleteMenuProduct.as_view(), name='delete-menu-product'),
    path(f'{API_BASE_URL}menu/categories', GetAddMenuCategories.as_view(), name='get-menu-categories'),
    path(f'{API_BASE_URL}menu/available', available_menu_items, name='available-menu-items'),
    path(f'{API_BASE_URL}menu/unavailable', unavailable_menu_items, name='unavailable-menu-items'),

    #products
    path(f'{API_BASE_URL}products', GetAddProducts.as_view(), name='get-add-products'),
    path(f'{API_BASE_URL}products/<int:id>', EditDeleteProduct.as_view(), name='edit-delete-product'),

    #promocodes
    path(f'{API_BASE_URL}promocodes', GetAddPromocodes.as_view(), name='get-add-promocodes'),
    path(f'{API_BASE_URL}promocodes/<id>', GetDeleteSpecificPromocode.as_view(), name='get-specific-promocode'),

    #tables
    path(f'{API_BASE_URL}tables', GetAddTables.as_view(), name='get-add-tables'),
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
    path(f'{API_BASE_URL}deliveries', GetAddDelivery.as_view(),name='get-add-delivery'),
    path(f'{API_BASE_URL}deliveries/client', GetAddClientDeliveries.as_view(),name='get-add-client-delivery'),
    path(f'{API_BASE_URL}deliveries/<int:id>', EditDeleteDelivery.as_view(), name='edit-delete-delivery'),
    path(f'{API_BASE_URL}deliveries/<int:delivery_id>/items', AddDeliveryMenu.as_view(),name='add-delivery-menu-items'),
    path(f'{API_BASE_URL}deliveries/<int:delivery_id>/items/<int:menu_id>',EditDeleteDeliveryMenu.as_view(),name='edit-delete-delivery-menu-item'),

    #storage
    path(f'{API_BASE_URL}storage', GetRetaurantProducts.as_view(), name = 'get-retaurant-products'),
    path(f'{API_BASE_URL}storage/increment', IncRestaurntProducts.as_view(), name = 'inc-restaurant-products'),
    path(f'{API_BASE_URL}storage/decrement', DecRestaurntProducts.as_view(), name = 'dec-restaurant-products'),

    #bookings
    path(f'{API_BASE_URL}bookings', GetAddBookings.as_view(), name = 'get-add-bookings'),
    path(f'{API_BASE_URL}bookings/<int:id>', EditDeleteBooking.as_view(), name='edit-delete-booking'),
    path(f'{API_BASE_URL}bookings/client', ClientGetAddBookings.as_view(), name='client-booking'),
]
