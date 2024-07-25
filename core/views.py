from django.shortcuts import render # Importuje funkci `render`, která se používá pro vykreslování šablon.
from django.views.generic import ListView, DetailView  # Importuje generické pohledy `ListView` a `DetailView`.
from django.shortcuts import get_object_or_404, redirect # Importuje funkce `get_object_or_404` pro získání objektu nebo vrácení 404 chyby a `redirect` pro přesměrování.
from django.urls import reverse # Importuje funkci `reverse` pro generování URL podle názvu cesty.
from core.forms import CheckoutForm, PaymentForm, DeliveryForm # Importuje formuláře
from core.models import Book, Cart, CartItem, Category, Address, Order, OrderItem, Customer # Importuje modely
from django.http import JsonResponse # Importuje JS
from random import shuffle # Importuje funkci `shuffle` pro zamíchání seznamu.
from django.utils import timezone  # Importuje `timezone` pro práci s časovými zónami.
from django.db.models import Q # Importuje `Q` pro složité dotazy v ORM.


class BooksView(ListView):
    template_name = 'books.html'
    model = Book

    def get_context_data(self, **kwargs): #get_context_data = připravuje a vrací data pro šablonu, self aktuální instance třídy, kwargs umoznuje dodatecne pridat klicove argumenty.
        context = super().get_context_data(**kwargs) # Získá výchozí kontext z nadřazené třídy ( super() ).
        context['categories'] = Category.objects.all() # Přidává všechny kategorie do kontextu.
        return context


class BookDetailView(DetailView):
    template_name = 'book_detail.html'
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_book = self.get_object() # Získá aktuální objekt. (knihu)
        
        related_books = list(Book.objects.filter(category=current_book.category).exclude(pk=current_book.pk)[:5])
        shuffle(related_books) # Zamíchá seznam souvisejících knih.
        
        context['related_books'] = related_books
        return context # Přidává související knihy do kontextu (šablony).


class BooksByCategoryView(ListView):
    template_name = 'books.html'
    model = Book

    def get_queryset(self): 
        return Book.objects.filter(category_id=self.kwargs['category_id'])  # Vrací queryset filtrující knihy podle ID kategorie.
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = Category.objects.get(id=self.kwargs['category_id'])
        return context


def show_about(request):
    return render(
        request,
        template_name='show_about.html',
        context={'names': ['Štěpán Kubíček', 'Kateřina Mladá']}
 )


def checkout(request):
    cart_id = request.session.get('cart_id') # Získá ID košíku ze session.
    if not cart_id: 
        return redirect('core:cart') # Pokud košík neexistuje, přesměruje na stránku s košíkem.

    cart = get_object_or_404(Cart, id=cart_id) # Získá košík podle ID.
    items = cart.cartitem_set.all()  # Získá všechny položky v košíku.

    # najdu posledni objednavku a stanovim si initial data
    last_order = Order.objects.filter(user=request.user).order_by('-placed_at').first()
    initial_data = {}
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
        form = CheckoutForm(request.POST)  # Pokud je metoda POST, zpracovává se odeslaný formulář.
        if form.is_valid():  # Pokud je formulář platný:
           
            customer, created = Customer.objects.get_or_create(
                email=form.cleaned_data['email'], # Hledá zákazníka podle e-mailu
                defaults={ # Používá tyto hodnoty, pokud se zákazník vytvoří
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                }
            )
            # Manualní uložení, protože se to špatně updatovalo
            customer.phone = form.cleaned_data['phone'] # Aktualizuje telefon zákazníka.
            customer.save()

            address = Address.objects.create(
                street=form.cleaned_data['street'],
                city=form.cleaned_data['city'],
                zip_code=form.cleaned_data['zip_code'],
                country=form.cleaned_data['country'],
                customer=customer
            )

            order = Order.objects.create( 
                customer=customer,   # Přiřazení zákazníka k objednávce
                payment_status=Order.PAYMENT_STATUS_PENDING, # Nastavení stavu platby na "čekající"
                
                
                total_cost=sum(item.quantity * item.book.unit_price for item in items),
                
                    # Vypočítání celkových nákladů objednávky na základě položek
                    # 'items' obsahuje seznam položek objednávky
                    # 'item.quantity' je množství knihy v položce
                    # 'item.book.unit_price' je jednotková cena knihy
                    # Celková cena se získá sečtením (sum) všech těchto nákladů
                
                user=request.user if request.user.is_authenticated else None,

                    # Přiřazení uživatele k objednávce, pokud je přihlášen
                    # Pokud uživatel není přihlášen, uloží se jako None
                
                
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
            return redirect('core:order_summary', order_id=order.id)  # Přesměruje na stránku shrnutí objednávky.

    else:
        form = CheckoutForm(initial=initial_data)  # Pokud je metoda GET, vytvoří prázdný formulář.

    total_price = sum(item.quantity * item.book.unit_price for item in items) # Vypočítá celkovou cenu.
    total_quantity = sum(item.quantity for item in items) # Vypočítá celkový počet položek.

    context = {
        'cart': cart,
        'items': items,
        'total_price': total_price,
        'total_quantity': total_quantity, 
        'form': form
    }
    return render(request, 'checkout.html', context)  # Vrátí šablonu s kontextem.


def order_success(request):
    return render(request, 'order_success.html')


# CART

def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id) # Získá knihu podle ID
    cart_id = request.session.get('cart_id') # Získá ID košíku ze session.
    if cart_id: 
        cart = get_object_or_404(Cart, id=cart_id) # Získá košík ID"
    else: # Pokud není k dispozici 
        cart = Cart.objects.create() # Vytvoří nový košík.
        request.session['cart_id'] = str(cart.id) # Uloží ID košíku do session.

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)

    if not item_created:
        cart_item.quantity += 1 # Pokud položka již existuje, zvýší množství.
        cart_item.save()

    return redirect('core:books')


def add_to_cart_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    cart_id = request.session.get('cart_id')
    if cart_id: # Pokud je k dispozici 
        cart = get_object_or_404(Cart, id=cart_id)
    else: # Pokud není k dispozici 
        cart = Cart.objects.create()
        request.session['cart_id'] = str(cart.id)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)
   
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('core:book_detail', pk=book.pk)

#STEJNE JAKO ADD TO CART, AKORAT TO FUNGUJE PRO DETAIL KNIHY

def cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id)
        items = cart.cartitem_set.all()  
        total_price = sum(item.quantity * item.book.unit_price for item in items)  # Vypočítá celkovou cenu.
        total_quantity = sum(item.quantity for item in items) # Vypočítá celkový počet položek.
    else: # Pokud není k dispozici 
        cart = None # že košík neexistuje
        items = [] # a je prázdný seznam pro položky v košíku
        total_price = 0 # nastaví se total price na 0
        total_quantity = 0  # stejně jako item q

    context = {
        'cart': cart,
        'items': items,
        'total_price': total_price,
        'total_quantity': total_quantity, 
    } # předávají se všechny hodnoty do šablony
    return render(request, 'cart.html', context)


def update_cart_item(request, book_id, action):
    cart_id = request.session.get('cart_id') 
    if not cart_id:
        return redirect(reverse('core:books'))
    cart = get_object_or_404(Cart, id=cart_id) # Získá košík podle ID
    cart_item = get_object_or_404(CartItem, cart=cart, book_id=book_id)  # Získá položku v košíku podle ID knihy.
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
    cart = get_object_or_404(Cart, id=cart_id) # Získá košík podle ID.
    cart_item = get_object_or_404(CartItem, cart=cart, book_id=book_id)  # Získá položku v košíku podle ID knihy.
    cart_item.delete() # Odstraní položku z košíku.
    return redirect(reverse('core:cart'))


def cart_count(request):
    cart_id = request.session.get('cart_id')  # Získá ID
    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id)
        total_quantity = sum(item.quantity for item in cart.cartitem_set.all())
    else:
        total_quantity = 0
    
    return JsonResponse({'count': total_quantity}) # Vrátí JSON (v base.js)


def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    customer = order.customer # Získá zákazníka k objednávce.
    items = order.orderitem_set.all() # Získá všechny položky v objednávce.
    address = Address.objects.filter(customer=customer).last()  # Získá poslední adresu zákazníka.

    if request.method == 'POST': # Pokud je metoda POST, zpracovává se odeslané formuláře.
        payment_form = PaymentForm(request.POST) # formuláře
        delivery_form = DeliveryForm(request.POST)

        if payment_form.is_valid() and delivery_form.is_valid(): # Pokud jsou oba formuláře platné
            return redirect('core:order_success')
    else:
        payment_form = PaymentForm() # Vytvoří prázdné formuláře.
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
    query = request.GET.get('q', '')  # Získá dotaz ze GET parametrů.
    if query:
        results = Book.objects.filter(
            Q(title__icontains=query) |  # Filtruje knihy podle názvu.
            Q(category__title__icontains=query) |  # Filtruje knihy podle kategorie.
            Q(authors__first_name__icontains=query) |  # Filtruje knihy podle jména autora.
            Q(authors__last_name__icontains=query)  # Filtruje knihy podle příjmení autora.
        ).distinct()
    else:
        results = Book.objects.none()

    return render(request, 'search_results.html', {'results': results, 'query': query})

# Q umoznuje kombinovat různé podmínky dotazů do jednoho q-setu