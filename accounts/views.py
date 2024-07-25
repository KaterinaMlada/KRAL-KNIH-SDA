from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from core.forms import UserRegisterForm, EditProfileForm
from core.models import Order


def login_view(request):
    if request.method == 'POST':  # Pokud je metoda POST, vytvoří se formulář s daty odeslanými v POST
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid(): # Pokud je formulář validní, získá se uživatel a přihlásí se
            user = form.get_user()
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = AuthenticationForm()
        # Pokud je metoda GET, vytvoří se prázdný formulář
    return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST': # Pokud je metoda POST, vytvoří se formulář s daty odeslanými v POST
        form = UserRegisterForm(request.POST)
        if form.is_valid():   
            form.save()  # Pokud je formulář validní, uloží se nový uživatel
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) # Získá se uživatelské jméno a heslo a provede se autentizace
            login(request, user) # Přihlášení nového uživatele
            return redirect('accounts:login')  
        

    else:  # Pokud je metoda GET, vytvoří se prázdný formulář
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('core:books')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user) # Pokud je metoda POST, vytvoří se formulář s daty odeslanými v POST
        if form.is_valid():
            form.save() # Pokud je formulář validní, uloží se změny profilu
            return redirect('accounts:profile')
    else:
        form = EditProfileForm(instance=request.user)    # Pokud je metoda GET, vytvoří se formulář s aktuálními údaji uživatele

    orders = Order.objects.filter(user=request.user)  # Získání objednávek uživatele
    
    return render(request, 'registration/profile.html', {'form': form, 'orders': orders})