from django import forms
from django.contrib.auth.password_validation import validate_password

from users.models import User, Profile
from shop.models import Order


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, label="Parol")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone']

    def clean_password(self):
        pwd = self.cleaned_data['password']
        validate_password(pwd)
        return pwd

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label="Login")
    password = forms.CharField(widget=forms.PasswordInput, label="Parol")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'date_of_birth', 'profile_picture', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
