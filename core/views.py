from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from core.forms import CheckoutForm, PaymentForm, DeliveryForm
from core.models import Book, Cart, CartItem, Category, Address, Order, OrderItem, Customer
from django.http import JsonResponse
from random import shuffle
from django.db.models import Q # Importuje `Q` pro složité dotazy v ORM.
from django.utils import timezone


class BooksView(ListView):
    template_name = 'books.html'
    model = Book

    def get_context_data(self, **kwargs):  # self aktuální instance třídy, kwargs umoznuje pridat klicove argumenty.
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
        shuffle(related_books) # Zamíchá seznam souvisejících knih.
        
        context['related_books'] = related_books
        return context


class BooksByCategoryView(ListView):
    template_name = 'books.html'
    model = Book

    def get_queryset(self): 
        return Book.objects.filter(category_id=self.kwargs['category_id'])  # Vrací queryset(seznam objektů)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = Category.objects.get(id=self.kwargs['category_id'])
        return context


def show_about(request):
    return render(
        request,
        template_name='show_about.html',
        context={'names': ['Štěpán Kubíček', 'Kateřina Mladá']})


def checkout(request):
    cart_id = request.session.get('cart_id') # Získá ID košíku ze session (uchovává informace o uživateli, obsah košíku)
    if not cart_id: 
        return redirect('core:cart')

    cart = get_object_or_404(Cart, id=cart_id)
    items = cart.cartitem_set.all()
    initial_data = {}
    if request.user.is_authenticated:
        # najdu posledni objednavku a stanovim si initial data
        last_order = Order.objects.filter(user=request.user).order_by('-placed_at').first()

        if last_order:
            # udelam si address protoze se k ni dostavam pres customera
            address = Address.objects.filter(customer=last_order.customer).first()
            initial_data = {
                'first_name': last_order.customer.first_name,
                'last_name': last_order.customer.last_name,
                'email': last_order.customer.email,
                'phone': last_order.customer.phone[3:],
                'street': address.street,
                'city': address.city,
                'zip_code': address.zip_code,
                'country': address.country,
                'prefix': '+421' if address.country == 'sk' else '+420',
            }

    if request.method == 'POST': 
        form = CheckoutForm(request.POST)  # Pokud je metoda POST tzn odeslání dat
        if form.is_valid():
           
            customer, created = Customer.objects.get_or_create(
                email=form.cleaned_data['email'],
                defaults={
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                }
            )
            # Manualní uložení, protože se to špatně updatovalo
            customer.phone = form.cleaned_data['phone']
            customer.save()

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
                
                
                total_cost=sum(item.quantity * item.book.unit_price for item in items),
                # Vypočítání celkových nákladů objednávky na základě položek

                user=request.user if request.user.is_authenticated else None,
                )

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                    unit_price=item.book.unit_price
                )

            cart.cartitem_set.all().delete() # Odstraní všechny položky z košíku.
            del request.session['cart_id']  # Odstraní ID košíku ze session.
            return redirect('core:order_summary', order_id=order.id)

    else:
        form = CheckoutForm(initial=initial_data)  # Pokud je metoda GET, vyplní data z poslední objednávky

    total_price = sum(item.quantity * item.book.unit_price for item in items)
    total_quantity = sum(item.quantity for item in items)

    context = {
        'cart': cart,
        'items': items,
        'total_price': total_price,
        'total_quantity': total_quantity, 
        'form': form
    }
    return render(request, 'checkout.html', context)


def order_success(request):
    return render(request, 'order_success.html')


# CART
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

# STEJNE JAKO ADD TO CART, AKORAT TO FUNGUJE PRO DETAIL KNIHY


def cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id)
        items = cart.cartitem_set.all()  
        total_price = sum(item.quantity * item.book.unit_price for item in items)
        total_quantity = sum(item.quantity for item in items)
    else:
        cart = None
        items = []
        total_price = 0
        total_quantity = 0

    context = {
        'cart': cart,
        'items': items,
        'total_price': total_price,
        'total_quantity': total_quantity, 
    }
    return render(request, 'cart.html', context)


def update_cart_item(request, book_id, action):
    cart_id = request.session.get('cart_id') 
    if not cart_id:
        return redirect(reverse('core:books'))
    cart = get_object_or_404(Cart, id=cart_id)
    cart_item = get_object_or_404(CartItem, cart=cart, book_id=book_id)
    if action == 'increase':
        cart_item.quantity += 1 # Pokud je akce 'increase', zvýší množství.
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1 # Pokud je akce 'decrease' a množství je větší než 1, sníží množství.
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
        total_quantity = sum(item.quantity for item in cart.cartitem_set.all())
    else:
        total_quantity = 0
    
    return JsonResponse({'count': total_quantity}) # Vrátí JSON (v base.js)


def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    customer = order.customer
    items = order.orderitem_set.all()
    address = Address.objects.filter(customer=customer).last()  # Získá poslední adresu zákazníka.

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        delivery_form = DeliveryForm(request.POST)

        if payment_form.is_valid() and delivery_form.is_valid():
            return redirect('core:order_success')
    else:
        payment_form = PaymentForm()
        delivery_form = DeliveryForm()

    context = {
        'order': order,
        'customer': customer,
        'address': address,
        'items': items,
        'payment_form': payment_form,
        'delivery_form': delivery_form,
    }
    return render(request, 'order_summary.html', context)


def search(request):
    query = request.GET.get('q', '')  # Získá dotaz z GET parametrů.
    if query:
        results = Book.objects.filter(  # icontains hleda bez citlivosti na velikost pismen
            Q(title__icontains=query) |
            Q(category__title__icontains=query) |
            Q(authors__first_name__icontains=query) |
            Q(authors__last_name__icontains=query)
        ).distinct()
    else:
        results = Book.objects.none()

    return render(request, 'search_results.html', {'results': results, 'query': query})

    # Q umoznuje kombinovat různé podmínky dotazů do jednoho q-setu
