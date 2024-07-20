from django import forms
from .models import Address


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=15)
    last_name = forms.CharField(max_length=25)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15, required=False)
    street = forms.CharField(max_length=50)
    city = forms.CharField(max_length=20)
    zip_code = forms.CharField(max_length=10)
    country = forms.CharField(max_length=15)


class PaymentForm(forms.Form):
    PAYMENT_METHOD_CHOICES = [
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('arrival', 'Payment Upon Arrival'),
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.RadioSelect)


class DeliveryForm(forms.Form):
    DELIVERY_METHOD_CHOICES = [
        ('address', 'Send to Address'),
        ('alza_box', 'Alza Box'),
        ('pickup', 'Personal Pickup'),
    ]
    delivery_method = forms.ChoiceField(choices=DELIVERY_METHOD_CHOICES, widget=forms.RadioSelect)


