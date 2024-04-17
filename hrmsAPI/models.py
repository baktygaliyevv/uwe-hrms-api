# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.utils import timezone
from django.db import models
import hashlib

class Bookings(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    table = models.ForeignKey('Tables', models.DO_NOTHING)
    persons = models.IntegerField()
    date = models.DateTimeField()
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bookings'


class Deliveries(models.Model):
    user = models.ForeignKey('Users', on_delete=models.SET_NULL, blank=True, null=True)
    restaurant = models.ForeignKey('Restaurants', models.DO_NOTHING)
    promocode = models.ForeignKey('Promocodes', models.DO_NOTHING, blank=True, null=True)
    address = models.TextField()
    created_at = models.DateTimeField()
    status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'deliveries'


class DeliveryMenu(models.Model):
    delivery = models.ForeignKey(Deliveries, models.DO_NOTHING)
    menu = models.ForeignKey('Menu', models.DO_NOTHING)
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'delivery_menu'


class EmailCodes(models.Model):
    code = models.CharField(primary_key=True, max_length=32)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    expiration_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'email_codes'

    def is_valid(self):
        return self.expiration_date > timezone.now()


class Menu(models.Model):
    menu_category = models.ForeignKey('MenuCategories', models.DO_NOTHING)
    name = models.TextField()
    price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'menu'


class MenuCategories(models.Model):
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'menu_categories'


class MenuProducts(models.Model):
    menu = models.ForeignKey(Menu, models.DO_NOTHING)
    product = models.ForeignKey('Products', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'menu_products'


class OrderMenu(models.Model):
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    menu = models.ForeignKey(Menu, models.DO_NOTHING)
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'order_menu'


class Orders(models.Model):
    user = models.ForeignKey('Users', on_delete=models.SET_NULL, blank=True, null=True)
    table = models.ForeignKey('Tables', models.DO_NOTHING)
    promocode = models.ForeignKey('Promocodes', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    complete_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class Products(models.Model):
    name = models.CharField(max_length=50)
    vegan = models.IntegerField()
    vegetarian = models.IntegerField()
    gluten_free = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'products'


class Promocodes(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    discount = models.IntegerField()
    valid_till = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'promocodes'


class RestaurantProducts(models.Model):
    restaurant = models.ForeignKey('Restaurants', models.DO_NOTHING)
    product = models.ForeignKey(Products, models.DO_NOTHING)
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'restaurant_products'


class Restaurants(models.Model):
    city = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'restaurants'


class Tables(models.Model):
    restaurant = models.ForeignKey(Restaurants, models.DO_NOTHING)
    capacity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tables'


class UserTokens(models.Model):
    token = models.CharField(primary_key=True, max_length=64)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    expiration_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_tokens'


class Users(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField()
    hash = models.CharField(max_length=128, blank=True, null=True)
    salt = models.CharField(max_length=32, blank=True, null=True)
    role = models.CharField(max_length=7)
    verified = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'users'

    def check_password(self, raw_password):
        """
        Manually check if the provided password matches the stored hashed password.
        Assumes you are storing a SHA-256 hashed password.
        """
        hashed_password = hashlib.sha256((raw_password + self.salt).encode('utf-8')).hexdigest()
        return self.hash == hashed_password