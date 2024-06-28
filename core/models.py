from django.contrib.auth.models import User, make_password

from django.db import models
from django.db.models import Model, CharField, IntegerField, EmailField, ForeignKey, ImageField, \
    DecimalField, ManyToManyField, DateTimeField  # doplnit postupne podle vsech modelu


class Author(models.Model):
    id = IntegerField(primary_key=True)
    first_name = CharField(max_length=15)
    last_name = CharField(max_length=25)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    name = CharField(max_length=15)

    def __str__(self):
        return f'{self.name}'


class Address(models.Model):
    country = CharField(max_length=15)
    city = CharField(max_length=15)
    street = CharField(max_length=15)
    zip_code = CharField(max_length=15)

    def __str__(self):
        return f'{self.country} {self.city} {self.street} {self.zip_code}'


class Role(models.Model):
    name = CharField(max_length=15)

    def __str__(self):
        return f'{self.name}'


class UserProfile(models.Model):
    login = EmailField(unique=True)
    password = CharField(max_length=150)
    address = ForeignKey(Address, on_delete=models.CASCADE)
    avatar = ImageField(upload_to='avatar')
    #TODO tady si moc nejsem jist , k obrazkum jsem se zatim nedostal
    role = ForeignKey(Role, on_delete=models.CASCADE)
    COMM_CHOICES = [
        ('mail', 'Mail'),
        ('email', 'Email'),
    ]
    pref_comm = CharField(max_length=150, choices=COMM_CHOICES)

    def __str__(self):
        return f'{self.login} {self.role}'

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
        # Toto by melo zahashovat heslo


class Book(models.Model):
    title = CharField(max_length=50)
    description = CharField(max_length=500)
    thumbnail = ImageField(upload_to='thumbnail')
    #TODO tady si nejsem jist proc v reamde je url
    category = ForeignKey(Category, on_delete=models.CASCADE)
    price = DecimalField(max_digits=5, decimal_places=2)
    product_type = CharField(max_length=50)
    #TODO tady asi v nasem pripade to bude typ vazby
    author = ManyToManyField(Author)

    def __str__(self):
        return f'{self.title} '


class OrderLine(models.Model):
    book = ForeignKey(Book, on_delete=models.CASCADE)
    quantity = IntegerField()
    price = DecimalField(max_digits=5, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.price = self.book.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.book} x {self.quantity} = {self.price}'


class Order(models.Model):
    user_name = ForeignKey(UserProfile, on_delete=models.PROTECT)
    total_cost = DecimalField(max_digits=5, decimal_places=2) #FIXME aby pocitala soucet
    user_address = ForeignKey(Address, on_delete=models.PROTECT)
    date_created = DateTimeField(auto_now_add=True)
    order_lines = ForeignKey(OrderLine, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.user_name} {self.date_created}'
