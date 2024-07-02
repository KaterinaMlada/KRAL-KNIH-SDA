from django.contrib.auth.models import User, make_password

from django.db import models
from django.db.models import Model, CharField, IntegerField, EmailField, ForeignKey, ImageField, \
    DecimalField, ManyToManyField, DateTimeField, TextField, DateField, \
    OneToOneField, PositiveSmallIntegerField  # doplnit postupne podle vsech modelu


class Promotion(Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Author(models.Model):
    id = IntegerField(primary_key=True)
    first_name = CharField(max_length=15)
    last_name = CharField(max_length=25)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


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
    
    first_name = CharField(max_length=15, default=None)
    last_name = CharField(max_length=25, default=None)
    email = EmailField(unique=True, default=None)
    phone = CharField(max_length=15, null=True)
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


class Address(models.Model):
    street = CharField(max_length=15)
    city = CharField(max_length=15)
    country = CharField(max_length=15)
    zip_code = CharField(max_length=15)
    customer = ForeignKey(Customer, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.country} {self.city} {self.street} {self.zip_code}'


class Category(models.Model):
    title = CharField(max_length=15)
    featured_book = ForeignKey('Book', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return f'{self.title}'


class Book(models.Model):
    title = CharField(max_length=50)
    slug = models.SlugField(default='-')
    description = TextField(max_length=500)
    unit_price = DecimalField(max_digits=6, decimal_places=2)
    inventory = IntegerField(default=0)
    category = ForeignKey(Category, on_delete=models.PROTECT)
    promotions = ManyToManyField(Promotion)
    authors = ManyToManyField(Author)
    """
    thumbnail = ImageField(upload_to='thumbnail')
    #TODO tady si nejsem jist proc v readme je url
    product_type = CharField(max_length=50)
    #TODO tady asi v nasem pripade to bude typ vazby
    
    """
    last_updated = DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} '

#Tady dole pokus o model OrderLine, ale jelikož si zatím nejsem jist co to je tak je schovaný :)
"""
class OrderLine(models.Model):
    book = ForeignKey(Book, on_delete=models.CASCADE)
    quantity = IntegerField()
    price = DecimalField(max_digits=5, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.price = self.book.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.book} x {self.quantity} = {self.price}'
"""


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
    customer = ForeignKey(Customer, on_delete=models.PROTECT)
    #PROTECT dávám, aby se ne nám nikdy nemazali objednávky, kvůli evidenci
    """
    total_cost = DecimalField(max_digits=5, decimal_places=2) #FIXME aby pocitala soucet
    order_lines = ForeignKey(OrderLine, on_delete=models.PROTECT)
    """

    def __str__(self):
        return f'Objednavka uzivatele {self.customer} z {self.placed_at}, {self.payment_status}'


class OrderItem(models.Model):
    order = ForeignKey(Order, on_delete=models.PROTECT)
    book = ForeignKey(Book, on_delete=models.PROTECT)
    quantity = PositiveSmallIntegerField()
    unit_price = DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    created_at = DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = ForeignKey(Cart, on_delete=models.CASCADE)
    book = ForeignKey(Book, on_delete=models.CASCADE)
    quantity = PositiveSmallIntegerField()
