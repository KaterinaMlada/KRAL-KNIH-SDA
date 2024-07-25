from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Address
from django import forms
from django.contrib.auth.models import User


class CheckoutForm(forms.Form):

    first_name = forms.CharField(
        max_length=50,
        label='Jméno',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vaše jméno'}))
   
    last_name = forms.CharField(
        max_length=50,
        label='Příjmení',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vaše příjmení'}))
    
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Váš e-mail'}))

    PREFIX_CHOICES = [
        ('+420', '+420'),
        ('+421', '+421'),
    ]

    prefix = forms.ChoiceField(
        choices=PREFIX_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        label='Předvolba'
        )

    phone = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Telefonní číslo',
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")'
        }),
        label='Telefon',
        required=False,
        error_messages={
            'invalid': 'Zadejte platné devítimístné telefonní číslo.'
        }
    )

    street = forms.CharField(
        max_length=50, 
        label='Ulice a číslo popisné',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ulice a číslo popisné'}))
   
    city = forms.CharField(
        max_length=20,
        label='Město',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Město'}))

    zip_code = forms.CharField(
        max_length=5,
        label='PSČ',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'PSČ',
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'  # bude možné psát pouze čísla
        }),
        validators=[RegexValidator(regex=r'^\d{5}$', message='PSČ musí obsahovat přesně 5 číslic')],

        # REGEX protože je to víc khůl a může začínat nulou
    )

    COUNTRY_CHOICES = [
        ('cz', 'Česká republika'),
        ('sk', 'Slovensko'),
    ]

    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        label='Země',
        widget=forms.Select(attrs={'class': 'form-control'} ))

    def clean(self):
        cleaned_data = super().clean()
        prefix = cleaned_data.get('prefix')
        phone = cleaned_data.get('phone')

        if prefix and phone:
            cleaned_data['phone'] = f"{prefix}{phone}" # Sloučí prefix a telefonní číslo do jednoho řetězce

        return cleaned_data


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

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="E-mail"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Tento e-mail už někdo používá.")  # Pokud e-mail existuje, chyba validace
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Hesla se neshodují.")

        return cleaned_data


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Jméno"
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Příjmení"
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="E-mail"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
