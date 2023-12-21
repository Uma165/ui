import os
from uuid import uuid4
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Product


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'isAdmin']


class UserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class ProductCreationForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image', 'name', 'description', 'price', 'stock_quantity', 'created_by']

    def __init__(self, user, *args, **kwargs):
        super(ProductCreationForm, self).__init__(*args, **kwargs)
        self.fields['created_by'].initial = user.username
        self.fields['created_by'].widget = forms.HiddenInput()

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Генерируем уникальное имя для изображения
        filename, extension = os.path.splitext(instance.image.name)
        unique_filename = f"{uuid4()}{extension}"

        instance.image.name = os.path.join('product_images', unique_filename)
        if commit:
            instance.save()
        return instance


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['created_by', 'image', 'name', 'description', 'price', 'stock_quantity']