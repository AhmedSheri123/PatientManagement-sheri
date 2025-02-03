from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import HospitalsModelForm, AdminUserModelForm, AdminUserProfileModelForm, SubscriptionsModelForm, UserSubscriptionModelForm
from accounts.models import HospitalsModel, UserProfile, AdminPermissionModel, SubscriptionsModel, UserSubscriptionModel
from dashboard.forms import AdminPermissionModelForm
from django.conf import settings
import os

# Create your views here.
BASE_DIR = settings.BASE_DIR

def index(request):
    return render(request, 'admin-panel/index.html')

def ManageHospitals(request):
    hospitals = HospitalsModel.objects.all()

    return render(request, 'admin-panel/hospitals/ManageHospitals.html', {'hospitals':hospitals})

def AddHospitals(request):
    form = HospitalsModelForm()
    if request.method == 'POST':
        form = HospitalsModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            hospital = form.save()
            os.mkdir(BASE_DIR / f'media/manager/{hospital.id}')
            return redirect('ManageHospitals')

    return render(request, 'admin-panel/hospitals/AddHospitals.html', {'form':form})

def EditHospitals(request, id):
    hospital = HospitalsModel.objects.get(id=id)

    form = HospitalsModelForm(instance=hospital)
    if request.method == 'POST':
        form = HospitalsModelForm(data=request.POST, files=request.FILES, instance=hospital)
        if form.is_valid():
            form.save()
            return redirect('ManageHospitals')

    return render(request, 'admin-panel/hospitals/EditHospitals.html', {'form':form})

def DeleteHospitals(request, id):
    hospital = HospitalsModel.objects.get(id=id)
    hospital.delete()
    return redirect('ManageHospitals')




def ManageHospitalAdmins(request):
    users = User.objects.filter(userprofile__profile_type='0')

    return render(request, 'admin-panel/hospital_admins/ManageHospitalAdmins.html', {'users':users})

def AddHospitalAdmins(request):
    form = AdminUserModelForm()
    form2 = AdminUserProfileModelForm()
    form3 = AdminPermissionModelForm()

    if request.method == 'POST':
        form = AdminUserModelForm(data=request.POST, files=request.FILES)
        form2 = AdminUserProfileModelForm(data=request.POST, files=request.FILES)
        form3 = AdminPermissionModelForm(data=request.POST)

        password = request.POST.get('password')
        if form.is_valid():
            user = form.save(commit=False)
            if password:
                user.set_password(password)
            user.save()

            perm = form3.save(commit=False)
            perm.save()
            userprofile = form2.save(commit=False)
            userprofile.user = user
            userprofile.permissions = perm
            userprofile.profile_type = '0'
            
            userprofile.save()
            
            return redirect('ManageHospitalAdmins')

    return render(request, 'admin-panel/hospital_admins/AddHospitalAdmins.html', {'form':form, 'form2':form2, 'form3':form3})

def EditHospitalAdmins(request, id):
    user = User.objects.get(id=id)
    userprofile = UserProfile.objects.get(user=user)
    perm = AdminPermissionModel.objects.get(id=userprofile.permissions.id)
    
    form = AdminUserModelForm(instance=user)
    form2 = AdminUserProfileModelForm(instance=userprofile)
    form3 = AdminPermissionModelForm(instance=perm)
    if request.method == 'POST':
        form = AdminUserModelForm(data=request.POST, files=request.FILES, instance=user)
        form2 = AdminUserProfileModelForm(data=request.POST, files=request.FILES, instance=userprofile)
        form3 = AdminPermissionModelForm(data=request.POST, instance=perm)
        password = request.POST.get('password')
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            user = form.save(commit=False)
            if password:
                user.set_password(password)
            user.save()
            form2.save()
            form3.save()
            return redirect('ManageHospitalAdmins')

    return render(request, 'admin-panel/hospital_admins/EditHospitalAdmins.html', {'form':form, 'form2':form2, 'form3':form3})

def DeleteHospitalAdmins(request, id):
    user = User.objects.get(id=id)
    userprofile = UserProfile.objects.get(user=user)
    permission = AdminPermissionModel(id=userprofile.permissions.id)
    user.delete()
    permission.delete()
    return redirect('ManageHospitalAdmins')


def ManageSubscriptions(request):
    subs = SubscriptionsModel.objects.filter()

    return render(request, 'admin-panel/subscriptions/ManageSubscriptions.html', {'subs':subs})

def AddSubscription(request):
    form = SubscriptionsModelForm()
    if request.method == 'POST':
        form = SubscriptionsModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ManageSubscriptions')
    return render(request, 'admin-panel/subscriptions/AddSubscription.html', {'form':form})

def EditSubscription(request, id):
    sub = SubscriptionsModel.objects.get(id=id)

    form = SubscriptionsModelForm(instance=sub)
    if request.method == 'POST':
        form = SubscriptionsModelForm(data=request.POST, files=request.FILES, instance=sub)
        if form.is_valid():
            form.save()
            return redirect('ManageSubscriptions')
    return render(request, 'admin-panel/subscriptions/EditSubscription.html', {'form':form})

def DeleteSubscription(request, id):
    sub = SubscriptionsModel.objects.get(id=id)
    sub.delete()
    return redirect('ManageSubscriptions')



def ManageUserSubscriptions(request):
    subs = UserSubscriptionModel.objects.filter()
    return render(request, 'admin-panel/user_subscriptions/ManageUserSubscriptions.html', {'subs':subs})

def AddUserSubscription(request):
    form = UserSubscriptionModelForm()
    if request.method == 'POST':
        form = UserSubscriptionModelForm(data=request.POST)
        if form.is_valid():
            hospital_id = request.POST.get('hospital_id')
            if hospital_id:
                user_subscription = form.save()
                hospital = HospitalsModel.objects.get(id=hospital_id)
                hospital.subscription = user_subscription
                hospital.save()
                return redirect('ManageUserSubscriptions')
    return render(request, 'admin-panel/user_subscriptions/AddUserSubscription.html', {'form':form})

def EditUserSubscription(request, id):
    sub = UserSubscriptionModel.objects.get(id=id)
    hospital = HospitalsModel.objects.get(subscription__id=sub.id)
    form = UserSubscriptionModelForm(instance=sub)
    if request.method == 'POST':
        form = UserSubscriptionModelForm(data=request.POST, instance=sub)
        if form.is_valid():
            form.save()
            return redirect('ManageUserSubscriptions')

    return render(request, 'admin-panel/user_subscriptions/EditUserSubscription.html', {'form':form, 'hospital':hospital})

def DeleteUserSubscription(request, id):
    sub = UserSubscriptionModel.objects.get(id=id)
    sub.delete()
    return redirect('ManageUserSubscriptions')
