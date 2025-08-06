from binascii import b2a_base64
from gc import set_debug

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_stuff = forms.BooleanField(required=True)

    class Meta:
        model = User

        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'is_stuff'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class BookForm(forms.ModelForm):
    pages = forms.IntegerField()
    is_published = forms.BooleanField()

    class Meta:
        model = Book

        fields = (
            'title',
            'author',
            'pages',
            'is_published',
            'status'
        )

    def save(self, commit=True):
        book = super().save(commit=False)
        book.pages = self.cleaned_data['pages']
        book.is_published = self.cleaned_data['is_published']
        if commit:
            book.save()
        return book
