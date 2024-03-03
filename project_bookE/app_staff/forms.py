from turtle import position
from django import forms
from django.forms import CharField
from django.forms import widgets
from .models import *


class StaffForm(forms.ModelForm):
    fullname = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
        'class': "form-control",
        'style': 'max-width: auto;border-color: #000000;',
    }))
    phone_number = forms.CharField(max_length=50,widget=forms.TextInput(attrs={
        'class': "form-control",
        'style': 'max-width: auto;border-color: #000000;',
    }))
    position = forms.CharField(max_length=50,widget=forms.TextInput(attrs={
        'class': "form-control",
        'style': 'max-width: auto;border-color: #000000;',
    }))
    salary = forms.FloatField(widget=forms.NumberInput(attrs={
        'class': "form-control",
        'style': 'max-width: auto;border-color: #000000;',
    }))
    email = forms.EmailField(max_length=50,widget=forms.TextInput(attrs={
        'class': "form-control",
        'style': 'max-width: auto;border-color: #000000;',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Nhập mật khẩu',
        'class': "form-control",
        'style': 'max-width: auto;border-color: #000000;',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Xác nhận mật khẩu',
        'class': "form-control",
        'style': 'max-width: auto;border-color: #000000;',
    }))
    note = forms.CharField(max_length=50,widget=forms.TextInput(attrs={
        'class': "form-control",
        'style': 'max-width: auto;border-color: #000000;',
    }))
    class Meta:
        model = Staff
        fields = ['fullname', 'phone_number', 'position','salary','email', 'password','note']

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields['fullname'].widget.attrs['placeholder'] = 'Họ tên'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Số điện thoại'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['position'].widget.attrs['placeholder'] = 'Vị trí'
        self.fields['salary'].widget.attrs['placeholder'] = 'Lương'
        self.fields['note'].widget.attrs['placeholder'] = 'Ghi chú'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(StaffForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Mật khẩu không khớp'
            )

class EditStaffForm(forms.Form):
    fullname = forms.CharField(label = "Họ tên",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    username = forms.CharField(label = "Tài Khoản",widget=forms.TextInput(attrs={
                    'class': "form-control",
                    'style': 'max-width: auto; border-color: #000000;',
                    

                    }))

    email = forms.EmailField(max_length=50,widget=forms.TextInput(attrs={
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
    position  = forms.CharField(label = "Vị trí",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    salary  = forms.CharField(label = "Lương",widget=forms.NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    dob = forms.DateField(label='Select a Date',widget=forms.DateInput(attrs={'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',}))

    note = forms.CharField(label = "Ghi chú",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    def __init__(self, *args, **kwargs):
        super(EditStaffForm, self).__init__(*args, **kwargs)
        # self.fields['email'].disabled = True
        # self.fields['username'].disabled = True
    
    class Meta:
        model = Staff
        fields = ['fullname','username', 'email', 'phone_number','gender','position','salary','dob', 'note' ]


class EditPersonalStaffForm(forms.Form):
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
    position  = forms.CharField(required= False,label = "Vị trí",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    salary  = forms.CharField(required= False,label = "Lương",widget=forms.NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    dob = forms.DateField(label='Select a Date',widget=forms.DateInput(attrs={'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',}))

    note = forms.CharField(required= False,label = "Ghi chú",widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: auto;border-color: #000000;',
                }))
    def __init__(self, *args, **kwargs):
        super(EditPersonalStaffForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        self.fields['username'].disabled = True
        self.fields['position'].disabled = True
        self.fields['salary'].disabled = True
        self.fields['note'].disabled = True
    
    class Meta:
        model = Staff
        fields = ['fullname','username', 'email', 'phone_number','gender','position','salary','dob', 'note' ]
