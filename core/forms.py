from django.contrib.auth.forms import UserCreationForm

from .models import Address
from django import forms
from django.contrib.auth.models import User


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


class UserRegisterForm(UserCreationForm):
    #Hazelo chybu ohledna hesla, vyreseno podedenim z preddefinovane tridy
    """
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Heslo"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Potvrzení hesla"
        )
    """

    email = forms.EmailField(
        required= True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="E-mail"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="First Name"
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Last Name"
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Email"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
