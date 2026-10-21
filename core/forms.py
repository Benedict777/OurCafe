from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import MenuItem, Order, Table


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'category', 'is_available']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table', 'items', 'status', 'note']
        widgets = {
            'items': forms.CheckboxSelectMultiple,
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'seats', 'is_available']