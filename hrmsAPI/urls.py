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
    ('users/', GetAllUsers),
    ('users/add', AddUser),
    ('users/<int:id>/', EditUser),
    ('users/<int:id>/delete/', DeleteUser),

    #menu
    ('menu/', GetMenuItems),
    ('menu/add', AddMenuItem),
    ('menu/<int:id>/', EditMenuItem),
    ('menu/<int:id>/', DeleteMenuItem),
    ('menu/<int:id>/products/', AddMenuProduct),
    ('menu/<int:id>/products/<int:productId>/', DeleteMenuProduct),
    ('menu/categories/', GetMenuCategories),
    ('menu/categories/', AddMenuCategory),

    #products
    ('products/', GetProducts),
    ('products/', AddProduct),
    ('products/<int:id>/', EditProduct),
    ('products/<int:id>/', DeleteProduct),

    #promocodes
    ('promocodes/', GetAllPromocodes),
    ('promocodes/add', AddPromocode),
    ('promocodes/<id>/', DeletePromocode),

    #tables
    ('tables/', GetAddTable),
    ('tables/<int:id>', EditDeleteTable),

    #auth
    ('auth/login/', LoginView),
]

router = routers.DefaultRouter()
for url, view in routes:
    router.register(url, view.as_view())

urlpatterns = [
    path(f'api/v{API_VERSION}/', include(router.urls))
]
