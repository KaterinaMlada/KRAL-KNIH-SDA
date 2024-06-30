from django.contrib.auth.models import User, make_password

from django.db import models
from django.db.models import Model, CharField, IntegerField, EmailField, ForeignKey, ImageField, \
    DecimalField, ManyToManyField, DateTimeField, TextField, DateField  # doplnit postupne podle vsech modelu


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


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = CharField(max_length=15)
    last_name = CharField(max_length=25)
    email = EmailField(unique=True)
    phone = CharField(max_length=15)
    birth_date = DateField(null=True)
    membership = CharField(max_length=15,choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    """
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

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
        # Toto by melo zahashovat heslo
        """

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'


class Book(models.Model):
    title = CharField(max_length=50)
    description = TextField(max_length=500)
    price = DecimalField(max_digits=6, decimal_places=2)
    inventory = IntegerField()
    """
    thumbnail = ImageField(upload_to='thumbnail')
    #TODO tady si nejsem jist proc v readme je url
    category = ForeignKey(Category, on_delete=models.CASCADE)
    product_type = CharField(max_length=50)
    #TODO tady asi v nasem pripade to bude typ vazby
    author = ManyToManyField(Author)
    """
    last_updated = DateTimeField(auto_now=True)

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
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]

    placed_at = DateTimeField(auto_now_add=True)
    payment_status = CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES)
    """
    user_name = ForeignKey(Customer, on_delete=models.PROTECT)
    total_cost = DecimalField(max_digits=5, decimal_places=2) #FIXME aby pocitala soucet
    user_address = ForeignKey(Address, on_delete=models.PROTECT)
    order_lines = ForeignKey(OrderLine, on_delete=models.PROTECT)
    """

    def __str__(self):
        return f'Objednavka z {self.placed_at}, {self.payment_status}'
