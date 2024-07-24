from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import (Model, CharField, IntegerField, EmailField, ForeignKey, DecimalField, ManyToManyField,
                              DateTimeField, TextField, DateField, PositiveSmallIntegerField, ImageField)
from uuid import uuid4


class Author(models.Model):
    first_name = CharField(max_length=15)
    last_name = CharField(max_length=25)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['last_name', 'first_name']


class Customer(models.Model):
    first_name = CharField(max_length=15, default=None)
    last_name = CharField(max_length=25, default=None)
    email = EmailField(unique=True, default=None)
    phone = CharField(max_length=15, null=True)
    birth_date = DateField(null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['last_name', 'first_name']


class Address(models.Model):
    street = CharField(max_length=50)
    city = CharField(max_length=20)
    zip_code = CharField(max_length=10)
    country = CharField(max_length=15)
    customer = ForeignKey(Customer, on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name_plural = "addresses"
        ordering = ['city', 'zip_code', 'country']

    def __str__(self):
        return f'{self.city} , {self.street}'


class Category(models.Model):
    title = CharField(max_length=15)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['title']

    def __str__(self):
        return f'{self.title}'


class Book(models.Model):
    title = CharField(max_length=50)
    slug = models.SlugField()
    description = TextField(max_length=500, null=True, blank=True)
    unit_price = DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory = IntegerField(
        default=0,
        validators=[MinValueValidator(1)])
    category = ForeignKey(Category, on_delete=models.PROTECT)
    authors = ManyToManyField(Author)
    thumbnail = ImageField(upload_to='images/', default='images/KK_logo.jpeg')
    last_updated = DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['title']


class Order(models.Model):
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_COMPLETE, 'Zaplaceno'),
        (PAYMENT_STATUS_PENDING, 'Čeká na zaplacení'),
        (PAYMENT_STATUS_FAILED, 'Platba selhala'),
    ]

    placed_at = DateTimeField(auto_now_add=True)
    payment_status = CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES)
    customer = ForeignKey(Customer, on_delete=models.PROTECT)
    total_cost = DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Objednavka {self.placed_at}, {self.payment_status}'

    class Meta:
        ordering = ['placed_at']


class OrderItem(models.Model):
    order = ForeignKey(Order, on_delete=models.PROTECT)
    book = ForeignKey(Book, on_delete=models.PROTECT)
    quantity = PositiveSmallIntegerField()
    unit_price = DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = DateTimeField(auto_now_add=True)
    customer = ForeignKey(Customer, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)

    def add_item(self, book, quantity=1):

        item, created = CartItem.objects.get_or_create(cart=self, book=book)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity  
        item.save()


class CartItem(models.Model): 
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.book.title}"
    
    @property  #Zajišťuje aby cena celkem vypisovala společnou částku pro více kusů stejné knihy. 
    def total_cost(self):
        return self.book.unit_price * self.quantity
