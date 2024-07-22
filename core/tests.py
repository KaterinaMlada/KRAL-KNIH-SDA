from django.test import TestCase
from .models import Cart, CartItem, Book, Customer, Category, Author
from .forms import UserRegisterForm

#models
class CartModelTestCase(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='Jirka',
            last_name='Prášek',
            email='Prasek@seznam.cz'
        )
        self.cart = Cart.objects.create(customer=self.customer)
        self.book = Book.objects.create(
            title='Kniha o me',
            slug='kniha-o-me',
            description='Kniha o mě a tátovi',
            unit_price=20,
            inventory=10,
            category=Category.objects.create(title='Fikce')
        )

    def test_cart_creation(self):
        self.assertEqual(self.cart.customer, self.customer)

    def test_add_item_to_cart(self):
        self.cart.add_item(self.book, quantity=2)
        cart_item = CartItem.objects.get(cart=self.cart, book=self.book)
        self.assertEqual(cart_item.quantity, 2)

        self.cart.add_item(self.book, quantity=3)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 5)

    def test_cart_string_representation(self):
        self.assertEqual(str(self.cart), str(self.cart.id))

#forms


class UserRegisterFormTestCase(TestCase):

    def test_form_valid_with_matching_passwords(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password': 'password123',
            'password_confirm': 'password123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_non_matching_passwords(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password': 'password123',
            'password_confirm': 'differentpassword',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

        self.assertIn('Passwords do not match', form.non_field_errors())

    def test_form_invalid_without_email(self):
        form_data = {
            'username': 'testuser',
            'password': 'password123',
            'password_confirm': 'password123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_invalid_without_username(self):
        form_data = {
            'email': 'testuser@gmail.com',
            'password': 'password123',
            'password_confirm': 'password123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_form_invalid_without_password(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password_confirm': 'password123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_form_invalid_without_password_confirm(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password': 'password123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password_confirm', form.errors)
