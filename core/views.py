from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from core.models import Book, Cart, CartItem

class BooksView(ListView):
    template_name = 'books.html'
    model = Book

class BookDetailView(DetailView):
    template_name = 'book_detail.html'
    model = Book

def show_about(request):
    return render(
        request,
        template_name='show_about.html',
        context={'names': ['Stepan Kubicek', 'Katerina Mlada']}
 )


def checkout(request):
    context = {}
    return render(request,'checkout.html', context)

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

    return redirect('core:cart')

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



