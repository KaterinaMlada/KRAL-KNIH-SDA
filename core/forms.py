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

   

