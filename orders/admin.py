from django.contrib import admin
from .models import *
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User

admin.site.site_header = 'Welcome Back Kelvin'


class OrderAdmin(admin.ModelAdmin):
    list_display = (
    'topic', 'service_type', 'academic_level', 'essay_type', 'number_of_pages', 'deadline', 'references',
    'number_of_references', 'customer', 'pub_date')
    list_filter = ('topic', 'service_type', 'academic_level', 'essay_type', 'number_of_pages', 'deadline', 'references',
                   'number_of_references', 'customer', 'pub_date')


class Writer(admin.ModelAdmin):
    list_display = ('first_name', 'second_name', 'phone', 'writer_quality', 'date_joined')
    list_filter = ('first_name', 'second_name', 'phone', 'writer_quality', 'date_joined')


class ClientDetails(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_joined',)
    list_filter = ('id', 'name', 'date_joined',)


class support(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_joined',)
    list_filter = ('id', 'name', 'date_joined',)


class Todo1(admin.ModelAdmin):
    list_display = ('Title', 'Description', 'deadline',)
    list_filter = ('Title', 'Description', 'deadline',)


class bidsOrder(admin.ModelAdmin):
    list_display = ('topic', 'comment')
    list_filter = ('topic', 'comment')


class ratings(admin.ModelAdmin):
    list_display = ('writerRating', 'service_rating', 'client_comment')
    list_filter = ('writerRating', 'service_rating', 'client_comment')


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user





@admin.register(Review)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'order', 'body', 'created', 'status')


# Now register the new UserAdmin...
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

admin.site.register(Order, OrderAdmin)
admin.site.register(Client, ClientDetails)
admin.site.register(Support, support)

admin.site.register(Writers, Writer)
