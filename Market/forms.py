from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Category, Product, Rating
from django.forms import modelform_factory, inlineformset_factory, modelformset_factory
from captcha.fields import CaptchaField

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_stuff = forms.BooleanField(required=True)
    captcha = CaptchaField(label='Введіть код з зображення')

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


ProductForm = modelform_factory(
    Product,
    fields=['name', 'price', 'category'],
    labels={'name': 'Назва продукту', 'price': 'Ціна продукту', 'category': 'Категорія'}
)

CategoryFormSet = modelformset_factory(
    Category,
    fields=['name'],
    extra=1,
    can_delete=True
)

ProductInlineFormSet = inlineformset_factory(
    Category,
    Product,
    fields=['name', 'price'],
    extra=2,
    can_delete=True
)

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']
        widgets = {
            'value': forms.RadioSelect(choices=[(i, '⭐' * i) for i in range(1, 6)])
        }
