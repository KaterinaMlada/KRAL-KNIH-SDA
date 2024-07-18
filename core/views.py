from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from core.forms import CheckoutForm
from core.models import Book, Cart, CartItem, Category, Address, Order, OrderItem, Customer
from django.http import JsonResponse
from random import shuffle
from django.utils import timezone

class BooksView(ListView):
    template_name = 'books.html'
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class BookDetailView(DetailView):
    template_name = 'book_detail.html'
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_book = self.get_object()
        
        related_books = list(Book.objects.filter(category=current_book.category).exclude(pk=current_book.pk)[:5])
        shuffle(related_books)
        
        context['related_books'] = related_books
        return context

class BooksByCategoryView(ListView):
    template_name = 'books.html'
    model = Book

    def get_queryset(self):
        return Book.objects.filter(category_id=self.kwargs['category_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = Category.objects.get(id=self.kwargs['category_id'])
        return context

def show_about(request):
    return render(
        request,
        template_name='show_about.html',
        context={'names': ['Štěpán Kubíček','Kateřina Mladá']}
 )


def checkout(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        return redirect('core:cart')

    cart = get_object_or_404(Cart, id=cart_id)
    items = cart.cartitem_set.all()

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
           
            customer, created = Customer.objects.get_or_create(
                email=form.cleaned_data['email'],
                defaults={
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'phone': form.cleaned_data['phone'],
                    'membership': Customer.MEMBERSHIP_BRONZE  # Default membership
                }
            )

           
            address = Address.objects.create(
                street=form.cleaned_data['street'],
                city=form.cleaned_data['city'],
                zip_code=form.cleaned_data['zip_code'],
                country=form.cleaned_data['country'],
                customer=customer
            )

          
            order = Order.objects.create(
                customer=customer,
                payment_status=Order.PAYMENT_STATUS_PENDING,
                total_cost=sum(item.quantity * item.book.unit_price for item in items)
            )

          
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                    unit_price=item.book.unit_price
                )

           
            cart.cartitem_set.all().delete()
            del request.session['cart_id']
            return redirect('core:order_success')

    else:
        form = CheckoutForm()

    total_price = sum(item.quantity * item.book.unit_price for item in items)

    context = {
        'cart': cart,
        'items': items,
        'total_price': total_price,
        'form': form
    }
    return render(request, 'checkout.html', context)


def order_success(request):
    return render(request, 'order_success.html')


#CART

def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id)
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = str(cart.id)



    
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)

    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('core:books')


def add_to_cart_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
 
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id)
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = str(cart.id)


    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)
    
   
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()


    return redirect('core:book_detail', pk=book.pk)


def cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id)
        items = cart.cartitem_set.all()  
        total_price = sum(item.quantity * item.book.unit_price for item in items)
    else:
        cart = None
        items = []
        total_price = 0

    context = {
        'cart': cart,
        'items': items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)


def update_cart_item(request, book_id, action):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        return redirect(reverse('core:books'))
    cart = get_object_or_404(Cart, id=cart_id)
    cart_item = get_object_or_404(CartItem, cart=cart, book_id=book_id)
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    return redirect(reverse('core:cart'))
    

def remove_from_cart(request, book_id):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        return redirect(reverse('core:books'))
    cart = get_object_or_404(Cart, id=cart_id)
    cart_item = get_object_or_404(CartItem, cart=cart, book_id=book_id)
    cart_item.delete()
    return redirect(reverse('core:cart'))



def cart_count(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id)
        cart_count = cart.cartitem_set.count()
    else:
        cart_count = 0
    return JsonResponse({'count': cart_count})