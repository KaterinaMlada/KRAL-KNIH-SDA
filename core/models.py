from django.contrib.auth.models import User  # Importuje model Django pro správu uživatelských účtů
from django.core.validators import MinValueValidator # Importuje validátory pro ověření minimální hodnoty
from django.db import models
from django.db.models import (Model, CharField, IntegerField, EmailField, ForeignKey, DecimalField, ManyToManyField,
                              DateTimeField, TextField, DateField, PositiveSmallIntegerField, ImageField)
from uuid import uuid4 # Importuje funkci pro generování unikátních identifikátorů


class Author(models.Model):
    first_name = CharField(max_length=15)
    last_name = CharField(max_length=25)

    def __str__(self):
        return f'{self.first_name} {self.last_name}' #vrací celé jméno

    class Meta:
        ordering = ['last_name', 'first_name']  # Řadí autory podle příjmení a pak křestního jména


class Customer(models.Model):
    first_name = CharField(max_length=15, default=None)
    last_name = CharField(max_length=25, default=None)
    email = EmailField(unique=True, default=None)
    phone = CharField(max_length=15, null=True)
    birth_date = DateField(null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}' # Vrátí celé jméno zákazníka


    class Meta:
        ordering = ['last_name', 'first_name'] # Řadí zákazníky podle příjmení a pak křestního jména
 

class Address(models.Model):
    street = CharField(max_length=50)
    city = CharField(max_length=20)
    zip_code = CharField(max_length=10)
    country = CharField(max_length=15)
    customer = ForeignKey(Customer, on_delete=models.CASCADE, default=None) # foreign- mnoho k jednomu, on_delete se odstrani všechny orders
    class Meta:
        verbose_name_plural = "addresses" #nastavuje množné jméno modelu
        ordering = ['city', 'zip_code', 'country'] # Řadí adresy podle města, PSČ a země
 
    def __str__(self):
        return f'{self.city} , {self.street}'


class Category(models.Model):
    title = CharField(max_length=15) # Název kategorie

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['title']

    def __str__(self):
        return f'{self.title}'


class Book(models.Model):
    title = CharField(max_length=50)
    slug = models.SlugField() # Slug pro URL knihy, slug prevadi z "ahoj svete" na ahoj-svete
    description = TextField(max_length=500, null=True, blank=True)
    unit_price = DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)]) # Cena knihy s minimální hodnotou 1
    inventory = IntegerField(
        default=0,
        validators=[MinValueValidator(1)])  # Počet knih na skladě s minimální hodnotou 1
    category = ForeignKey(Category, on_delete=models.PROTECT)  # foreign- mnoho k jednomu, ondelete protect zakazuje odstranění kategorie, pokud existují produkty, které na ni odkazují
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

    placed_at = DateTimeField(auto_now_add=True) # Datum a čas vytvoření objednávky
    payment_status = CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES)
    customer = ForeignKey(Customer, on_delete=models.PROTECT) # foreign- mnoho k jednomu, ondelete protect zakazuje odstranění kategorie, pokud existují produkty, které na ni odkazují
    total_cost = DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) #nastaví hodnotu `category` na NULL, pokud je odpovídající kategorie odstraněna

    def __str__(self):
        return f'Objednavka {self.placed_at}, {self.payment_status}'

    class Meta:
        ordering = ['placed_at']  # Řadí objednávky podle data a času vytvoření


class OrderItem(models.Model):
    order = ForeignKey(Order, on_delete=models.PROTECT)
    book = ForeignKey(Book, on_delete=models.PROTECT)
    quantity = PositiveSmallIntegerField()
    unit_price = DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)  # Unikátní ID košíku
    created_at = DateTimeField(auto_now_add=True)
    customer = ForeignKey(Customer, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)

    def add_item(self, book, quantity=1):
  # Přidá položku do košíku nebo aktualizuje množství, pokud již existuje
        item, created = CartItem.objects.get_or_create(cart=self, book=book)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity  
        item.save()


class CartItem(models.Model): 
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) # Cizí klíč na košík
    book = models.ForeignKey(Book, on_delete=models.CASCADE) # Cizí klíč na knihu
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.book.title}"
    
    @property  #Zajišťuje aby cena celkem vypisovala společnou částku pro více kusů stejné knihy. 
    def total_cost(self):
        return self.book.unit_price * self.quantity
