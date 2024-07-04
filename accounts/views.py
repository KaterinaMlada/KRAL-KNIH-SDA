from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.transaction import atomic
from django.forms import DateField, CharField, Textarea, NumberInput
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.models import Profile


class SubmittableLoginView(LoginView):
    template_name = 'login.html'


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

    date_of_birth = DateField(widget=NumberInput(attrs={'type': 'date'}))
    biography = CharField(label='About me..', widget=Textarea)

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        user = super().save(commit)  
        date_of_birth = self.cleaned_data['date_of_birth']  
        biography = self.cleaned_data['biography']
        profile = Profile(user=user, date_of_birth=date_of_birth, biography=biography)  
        if commit:
            profile.save()
        return user


class SignUpView(CreateView):
    template_name = 'acc.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home')


class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'acc.html'
    success_url = reverse_lazy('home')

