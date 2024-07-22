from django import forms
from .models import Address


from django import forms


class CheckoutForm(forms.Form):
    first_name = forms.CharField(
        max_length=15, 
        label='Jméno',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vaše jméno'}))
   
    last_name = forms.CharField(
        max_length=25, 
        label='Příjmení',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vaše příjmení'}))
    
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Váš e-mail'}))
    
    phone = forms.CharField(
        max_length=15, 
        required=False, 
        label='Telefon',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vaše telefonní číslo'}))
    
    street = forms.CharField(
        max_length=50, 
        label='Ulice a číslo popisné',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ulice a číslo popisné'}))
   
    city = forms.CharField(
        max_length=20,
        label='Město',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Město'}))
   
    zip_code = forms.CharField(
        max_length=10, 
        label='PSČ',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PSČ'}) )
    
    country = forms.CharField(
        max_length=15, 
        label='Země',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Země'}) )


class PaymentForm(forms.Form):
    PAYMENT_METHOD_CHOICES = [
        ('paypal', 'PayPal'),
        ('bank_card', 'Platební karta'),
        ('arrival', 'Dobírka'),
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.RadioSelect)


class DeliveryForm(forms.Form):
    DELIVERY_METHOD_CHOICES = [
        ('ppl', 'PPL'),
        ('ceska_posta', 'Česká Pošta'),
        ('pickup', 'Vyzvednu na prodejně'),
    ]
    delivery_method = forms.ChoiceField(choices=DELIVERY_METHOD_CHOICES, widget=forms.RadioSelect)


