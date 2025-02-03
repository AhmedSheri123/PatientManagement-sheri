from django import forms
from accounts.models import HospitalsModel, UserProfile, SubscriptionsModel, UserSubscriptionModel
from django.contrib.auth.models import User

class HospitalsModelForm(forms.ModelForm):
    class Meta:
        model = HospitalsModel
        exclude = ['img_base64', 'subscription']


class AdminUserProfileModelForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'gender', 'hospital_profile']

class AdminUserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class SubscriptionsModelForm(forms.ModelForm):
    class Meta:
        model = SubscriptionsModel
        fields = '__all__'
        widgets = {
            'creation_date':forms.DateTimeInput(attrs={'type':'datetime-local'})
        }

class UserSubscriptionModelForm(forms.ModelForm):
    class Meta:
        model = UserSubscriptionModel
        fields = '__all__'
        widgets = {
            'creation_date':forms.DateTimeInput(attrs={'type':'datetime-local'})
        }
