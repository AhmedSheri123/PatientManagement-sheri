from django import forms
from .models import AdminPermissionModel
from accounts.models import UserProfile
from django.contrib.auth.models import User

class AdminPermissionModelForm(forms.ModelForm):

    class Meta:
        model = AdminPermissionModel
        fields = '__all__'


class UserProfileModelForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['account_alias_name', 'phone', 'gender']

class UserModelForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
