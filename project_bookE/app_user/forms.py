from django import forms
from django.forms import CharField
from django.forms import widgets
from .models import *


class RegisterForm(forms.ModelForm):
    fullname = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password'
    }))

    class Meta:
        model = Customer
        fields = ['fullname', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['fullname'].widget.attrs['placeholder'] = 'Họ tên'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Số điện thoại'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Mật khẩu không khớp'
            )

class EditProfileForm(forms.Form):
    fullname = forms.CharField(label = "Họ tên",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    username = forms.CharField(required= False,label = "Tài Khoản",widget=forms.TextInput(attrs={
                    'class': "form-control",
                    'style': 'max-width: auto; border-color: #000000;',
                    

                    }))

    email = forms.EmailField(required=False,max_length=50,widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    phone_number = forms.CharField(label = "Số điện thoại",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    gender = forms.CharField(label = "Giới tính",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    dob = forms.DateField(label='Select a Date',widget=forms.DateInput(attrs={'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',}))


    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        self.fields['username'].disabled = True
    
    class Meta:
        model = Customer
        fields = ['fullname','username', 'email', 'phone_number','gender','dob' ]


class AddressShippingForm(forms.ModelForm):
    name_receiver  = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    receiver_phone = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    city = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    district  = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    ward = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    address_detail = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))

    class Meta:
        model = AddressShipping
        fields = ['name_receiver', 'receiver_phone', 'city', 'district', 'ward', 'address_detail']