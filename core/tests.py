from django.test import TestCase
from .models import Cart, CartItem, Book, Customer, Category
from django.contrib.auth.models import User
from .forms import EditProfileForm
from django.urls import reverse
from django.utils import timezone



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


class EditProfileFormTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='test123',
            first_name='Adam',
            last_name='Mnich',
            email='test@seznam.cz'
        )

    def test_form_valid_data(self):
        form = EditProfileForm(data={
            'first_name': 'Novy',
            'last_name': 'Mnisek',
            'email': 'novaadresa@seznam.cz'
        })
        self.assertTrue(form.is_valid())

    def test_form_empty_optional_fields(self):
        form = EditProfileForm(data={
            'first_name': 'Novy',
            'last_name': '',
            'email': 'novaadresa@seznam.cz'
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_email(self):
        form = EditProfileForm(data={
            'first_name': 'Novy',
            'last_name': 'Mnisek',
            'email': 'spatnyemail'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_required_email(self):
        form = EditProfileForm(data={
            'first_name': 'Novy',
            'last_name': 'Mnisek',
            'email': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_initial_data(self):
        form = EditProfileForm(instance=self.user)
        self.assertEqual(form.initial['first_name'], 'Adam')
        self.assertEqual(form.initial['last_name'], 'Mnich')
        self.assertEqual(form.initial['email'], 'test@seznam.cz')

if __name__ == "__main__":
    import unittest
    unittest.main()


    