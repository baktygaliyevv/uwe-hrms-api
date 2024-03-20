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
from django.urls import path, include
from django.http import HttpResponse
from rest_framework import routers
from .methods.users.views import AddUser, GetAllUsers, EditUser, DeleteUser
from .methods.menu.views import GetMenuItems, AddMenuItem, EditMenuItem, DeleteMenuItem, AddMenuCategory, AddMenuProduct, DeleteMenuProduct, GetMenuCategories
from .methods.products.views import GetProducts, AddProduct, DeleteProduct, EditProduct
from .methods.promocodes.views import GetAllPromocodes, AddPromocode, DeletePromocode
from .methods.tables.views import GetAddTable, EditDeleteTable
from .methods.auth.views import LoginView

API_VERSION = '1'

routes = [
    # users
    ('users/', GetAllUsers, 'GetAllUsers'),
    ('users/add', AddUser, 'AddUser'),
    ('users/<int:id>/', EditUser, 'EditUser'),
    ('users/<int:id>/delete/', DeleteUser, 'DeleteUser'),

    #menu
    ('menu/', GetMenuItems, 'GetMenuItems'),
    ('menu/add', AddMenuItem, 'AddMenuItem'),
    ('menu/<int:id>/', EditMenuItem, 'EditMenuItem'),
    ('menu/<int:id>/', DeleteMenuItem, 'DeleteMenuItem'),
    ('menu/<int:id>/products/', AddMenuProduct, 'AddMenuProduct'),
    ('menu/<int:id>/products/<int:productId>/', DeleteMenuProduct, 'DeleteMenuProduct'),
    ('menu/categories/', GetMenuCategories, 'GetMenuCategories'),
    ('menu/categories/', AddMenuCategory, 'AddMenuCategory'),

    #products
    ('products/', GetProducts, 'GetProducts'),
    ('products/', AddProduct, 'AddProduct'),
    ('products/<int:id>/', EditProduct, 'EditProduct'),
    ('products/<int:id>/', DeleteProduct, 'DeleteProduct'),

    #promocodes
    ('promocodes/', GetAllPromocodes, 'GetAllPromocodes'),
    ('promocodes/add', AddPromocode, 'AddPromocode'),
    ('promocodes/<id>/', DeletePromocode, 'DeletePromocode'),

    #tables
    ('tables/', GetAddTable, 'GetAddTable'),
    ('tables/<int:id>', EditDeleteTable, 'EditDeleteTable'),

    #auth
    ('auth/login/', LoginView, 'LoginView'),
]

router = routers.DefaultRouter()
for url, view, basename in routes:
    router.register(url, view.as_view(), basename=basename)

urlpatterns = [
    path(f'api/v{API_VERSION}/', include(router.urls))
]
