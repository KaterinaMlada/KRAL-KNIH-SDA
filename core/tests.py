from django.test import TestCase, SimpleTestCase, Client
from .models import Cart, CartItem, Book, Customer, Category
from django.contrib.auth.models import User
from .forms import EditProfileForm
from django.urls import reverse, resolve
from core.views import *



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


# URL testy

class URLTests(SimpleTestCase):

    def test_books_url(self):
        url = reverse('core:books')
        self.assertEqual(resolve(url).func.view_class, BooksView)

    def test_book_detail_url(self):
        url = reverse('core:book_detail', args=['1'])
        self.assertEqual(resolve(url).func.view_class, BookDetailView)


# VIEW testy

class BooksViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(title='Test Category')
        self.book = Book.objects.create(
            title='Test Book',
            category=self.category,
            unit_price=10.00
        )

    def test_books_view(self):
        response = self.client.get(reverse('core:books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books.html')
        self.assertIn('categories', response.context)
        self.assertIn('object_list', response.context)
        self.assertContains(response, self.book.title)


class BookDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(title='Test Category')
        self.book = Book.objects.create(
            title='Test Book',
            category=self.category,
            unit_price=10.00
        )

    def test_book_detail_view(self):
        response = self.client.get(reverse('core:book_detail', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_detail.html')
        self.assertIn('object', response.context)
        self.assertIn('related_books', response.context)
        self.assertContains(response, self.book.title)
