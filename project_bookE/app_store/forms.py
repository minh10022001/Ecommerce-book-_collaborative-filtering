from django import forms
from .views import *
from .models import *

class RatingForm(forms.ModelForm):
    class Meta:
        model = RatingBook
        fields = ["content", "rating"]

class ImportForm(forms.ModelForm):
    class Meta:
        model = ImportBook
        fields = ["price_import", "price_sale","num"]

class BookForm(forms.ModelForm):
   
    name = forms.CharField(required=False,label = "Tên sách", widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto; border-color: #000000;',

                }))
    price = forms.FloatField(required=False,label = "Giá bán",widget=forms.NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto; border-color: #000000;color:black;',

                }))
    short_description = forms.CharField(required=False,label = "Nôi dung chính", widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto; border-color: #000000;',

                }))
    author = forms.CharField(required=False,label = "Tác giả", widget=forms.TextInput(attrs={
        'class': "form-control",
        'style': 'max-width: auto; border-color: #000000;',

        }))
    slug = forms.CharField(required=False,label = "Slug", widget=forms.TextInput(attrs={
        'class': "form-control",
        'style': 'max-width: auto; border-color: #000000;',

    }))
    is_authenic = forms.CharField(required=False,label = "Chính hãng", widget=forms.TextInput(attrs={
        'class': "form-control",
        'style': 'max-width: auto; border-color: #000000;',

        }))
    publisher  = forms.CharField(required=False,label = "Nhà xuất bản", widget=forms.TextInput(attrs={
        'class': "form-control",
        'style': 'max-width: auto; border-color: #000000;',

    }))
    publication_year= forms.IntegerField(required=False, label = "Năm xuất bản",widget=forms.NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto; border-color: #000000;'
                }))
    dimensions = forms.CharField(required=False,label = "Kích thước", widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto; border-color: #000000; color:black;',

                }))
    book_cover = forms.CharField(required=False,label = "Loại bìa", widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto; border-color: #000000;',

                }))
    numpage  = forms.CharField(required=False,label = "Số trang", widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto; border-color: #000000;',

                }))
    manufacturer = forms.CharField(required=False,label = "Công ty phát hành", widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto; border-color: #000000;',

                }))
    images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True,
        'style': 'max-width: auto; border-color: #000000;',
    }))


    class Meta:
        model = Book
        fields = ["name","price","short_description","author","slug","is_authenic","publisher","publication_year","dimensions","book_cover","numpage","manufacturer","images"]
