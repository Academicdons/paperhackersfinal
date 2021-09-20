from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', ]


class TakeOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['writer', 'bid_statement']
        widgets = {'writer': forms.Select(attrs={'readonly': 'readonly'}),
                   'bid_statement': forms.Textarea(attrs={'class': 'form-control'}),
                   }


class CreateprofileForm(ModelForm):
    class Meta:
        model = Writers
        fields = [
            'first_name', 'second_name', 'user',
            'pseudonym', 'city', 'description', 'gender', 'phone', 'country',
            'university', 'unidept', 'statement','image',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput,
            'second_name': forms.TextInput(attrs={'class': 'form-control'}),
            'pseudonym': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'university': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'statement': forms.Textarea(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'readonly': 'readonly'}),

        }


class ClientorderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'topic', 'service_type', 'academic_level', 'customer', 'essay_type', 'subject', 'number_of_pages',
            'deadline',
            'spacing',
            'Paper_Instruction', 'references', 'file_upload', 'number_of_references')
        Widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'custom-select'}),
            'academic_level': forms.Select(attrs={'id': 'dropdownMenuButton', 'aria-haspopup': 'true',
                                                  'class': 'btn btn-secondary dropdown-toggle w-100 p-3',
                                                  'type': 'button'}),
            'essay_type': forms.Select(attrs={'class': 'custom-select'}),
            'subject': forms.Select(attrs={'class': 'custom-select'}),
            'number_of_pages': forms.IntegerField,  # (attrs={'class' : 'input-group-text'}),
            'deadline': forms.Select(attrs={'class': 'form-control'}),
            'Paper_Instruction': forms.Textarea(attrs={'class': 'form-control', 'style': 'width:100%;'}),
            'references': forms.Select(attrs={'class': 'custom-select'}),
            'spacing': forms.Select(attrs={'class': 'custom-select'}),
            'file_upload': forms.FileField,  # (attrs={'class' : 'form-control-file'}),
            'number_of_references': forms.IntegerField,  # (attrs={'class' : 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-control-plaintext'}),
        }

    # def __init__(self, *args, **kwargs):
    #   super().__init__(*args, **kwargs)
class AdminOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('topic', 'service_type', 'academic_level', 'Paper_Instruction',
                  'references', 'file_upload', 'number_of_references',
                  'essay_type', 'subject', 'number_of_pages', 'deadline')


class adminUpdateorderForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            'order_status', 'writer'
        ]

    widgets = {
        'writer': forms.Select(attrs={'class': 'form-control'}),
        'order_status': forms.Select(attrs={'class': 'form-control'}),
    }


class CreateUserFormss(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']




class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['country', 'user']


class WriterForm(ModelForm):
    class Meta:
        model = Writers
        fields = '__all__'


class WritercompleteOrder(ModelForm):
    class Meta:
        model = Order
        fields = [
            'order_status',
        ]

    widgets = {
        'order_status': forms.Select(attrs={'class': 'form-control'}),
    }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
