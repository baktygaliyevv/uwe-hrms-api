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
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from .methods.users.views import AddUser, GetAllUsers, EditUser, DeleteUser
from .methods.menu.views import GetMenuItems, AddMenuItem, EditMenuItem, DeleteMenuItem, AddMenuCategory, AddMenuProduct, DeleteMenuProduct, GetMenuCategories
from .methods.products.views import GetProducts, AddProduct, DeleteProduct, EditProduct
from .methods.promocodes.views import GetAllPromocodes, AddPromocode, DeletePromocode
from .methods.tables.views import GetAddTable, EditDeleteTable
from .methods.auth.views import LoginView

def ping_view(request):
    return HttpResponse("pong", status=200)

urlpatterns = [
    path('', ping_view, name='ping'),
    path('ping/', ping_view, name='ping'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    #users
    path('users/', GetAllUsers.as_view(), name='get-users'),
    path('users/add', AddUser.as_view(), name='add-users'),
    path('users/<int:id>/', EditUser.as_view(), name='edit-user'),
    path('users/<int:id>/delete/', DeleteUser.as_view(), name='delete-user'),

    #menu
    path('menu/', GetMenuItems.as_view(), name='get-menu-item'),
    path('menu/add', AddMenuItem.as_view(), name='add-menu-item'),
    path('menu/<int:id>/', EditMenuItem.as_view(), name='edit-menu-item'),
    path('menu/<int:id>/', DeleteMenuItem.as_view(), name='delete-menu-item'),
    path('menu/<int:id>/products/', AddMenuProduct.as_view(), name='add-menu-product'),
    path('menu/<int:id>/products/<int:productId>/', DeleteMenuProduct.as_view(), name='delete-menu-product'),
    path('menu/categories/', GetMenuCategories.as_view(), name='get-menu-categories'),
    path('menu/categories/', AddMenuCategory.as_view(), name='add-menu-category'),

    #products
    path('products/', GetProducts.as_view(), name='get-products'),
    path('products/', AddProduct.as_view(), name='add-product'),
    path('products/<int:id>/', EditProduct.as_view(), name='edit-product'),
    path('products/<int:id>/', DeleteProduct.as_view(), name='delete-product'),

    #promocodes
    path('promocodes/', GetAllPromocodes.as_view(), name='get-promocodes'),
    path('promocodes/add', AddPromocode.as_view(), name='add-promocode'),
    path('promocodes/<id>/', DeletePromocode.as_view(), name='delete-promocode'),

    #tables
    path('tables/', GetAddTable.as_view(), name='get-add-tables'),
    path('tables/<int:id>', EditDeleteTable.as_view(), name='edit-delete-table'),

    #auth
    path('auth/login/', LoginView.as_view(), name='login'),
]
