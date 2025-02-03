from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from dashboard.libs import get_general_settings
from django.utils import translation
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SubscriptionsModel
from accounts.models import HospitalsModel, UserProfile, UserSubscriptionModel, SubscriptionsModel, PatientVistorModel, PatientMedicalReportModel
from django.db.models import Q
import os
# Create your views here.
BASE_DIR = settings.BASE_DIR

def index(request):
    return redirect('Login')

def Login(request):
    file_path = str(BASE_DIR / 'dashboard/settings.json')
    settings, img_obj = get_general_settings(file_path)
    username = request.GET.get('username', '')
    if request.method == 'POST':
        login_type = request.POST.get('type')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if login_type == '2':
            users = User.objects.filter(email=email)
        else:
            users = User.objects.filter(username=username)
        if users.exists():
            user = users.first()
            username = user.username
            auth_user = authenticate(request, username=username, password=password)
            if auth_user is not None:

                has_userprofile = False
                is_employee = False
                try:
                    userprofile = user.userprofile
                    has_userprofile = True
                except:pass

                if has_userprofile:
                    is_employee = userprofile.profile_type == '2' or userprofile.profile_type == '0'
            
                if user.is_superuser:
                    login(request, user)
                    return redirect('admin_panel_index')
                
                elif is_employee:
                    login(request, user)
                    translation.activate(userprofile.hospital_profile.lang)
                    return redirect('PanelHome')
                

    return render(request, 'accounts/login/login.html', {'img_obj':img_obj, 'settings':settings, 'username':username})

def Logout(request):
    logout(request)
    return redirect('Login')

def get_discont_original_price_and_saved_money(price, discont):
    orginal = None
    if price and discont:
        orginal = (price/ (100-discont))*100
        return int(orginal), int(orginal-price)
    return orginal, None

@csrf_exempt
def GetSubscriptionsPlanInfoAPI(request):
    subscriptions_data = []
    subscriptions = SubscriptionsModel.objects.filter(is_enabled=True)
    id = request.GET.get('id')
    if id:
        subscriptions = subscriptions.filter(id=id)
        
    for subscription in subscriptions:
        data = {}
        #baisc data
        data['id'] = subscription.id
        data['title'] = subscription.title
        data['subtitle'] = subscription.subtitle
        data['theme'] = {
            "type":subscription.plan_type,
            "theme":subscription.Theem
        }

        #price
        monthly_orignal_price, monthly_saved_price = get_discont_original_price_and_saved_money(subscription.price_monthly, subscription.discont_monthly)
        yearly_orignal_price, yearly_saved_price = get_discont_original_price_and_saved_money(subscription.price_yearly, subscription.discont_yearly)
        data['price'] = {
            "monthly": {
                "value": subscription.price_monthly,
                "orignal_price": monthly_orignal_price,
                "save_value": monthly_saved_price,
                "discont": subscription.discont_monthly
            },
            "yearly": {
                "value": subscription.price_yearly,
                "orignal_price": yearly_orignal_price,
                "save_value": yearly_saved_price,
                "discont": subscription.discont_yearly
            }
        }
        def get_field_verbose_name(field_name):
            return subscription._meta.get_field(field_name).verbose_name.title()
        
        #features
        data['features'] = [
            {
                "name": get_field_verbose_name('number_of_patient'),
                "type": "num",
                "value": subscription.number_of_patient
            },
            {
                "name": get_field_verbose_name('number_of_local_visit'),
                "type": "num",
                "value": subscription.number_of_local_visit
            },
            {
                "name": get_field_verbose_name('number_of_home_visit'),
                "type": "num",
                "value": subscription.number_of_home_visit
            },
            {
                "name": get_field_verbose_name('hosptial_storage_size_mb'),
                "type": "num",
                "value": str(subscription.hosptial_storage_size_mb) + 'MB'
            },
            {
                "name": get_field_verbose_name('number_of_visit_medical_reports'),
                "type": "num",
                "value": subscription.number_of_visit_medical_reports
            },
            {
                "name": get_field_verbose_name('number_of_customize_medical_tests'),
                "type": "num",
                "value": subscription.number_of_customize_medical_tests
            },
            {
                "name": get_field_verbose_name('number_of_medical_tests_reports'),
                "type": "num",
                "value": subscription.number_of_medical_tests_reports
            },
            {
                "name": get_field_verbose_name('number_of_manager'),
                "type": "num",
                "value": subscription.number_of_manager
            },
            {
                "name": get_field_verbose_name('one_to_one_chat'),
                "type": "bool",
                "value": subscription.one_to_one_chat
            },
            {
                "name": get_field_verbose_name('extract_patient_info'),
                "type": "bool",
                "value": subscription.extract_patient_info
            },
            {
                "name": get_field_verbose_name('live_chat_with_support'),
                "type": "bool",
                "value": subscription.live_chat_with_support
            },
        ]
        subscriptions_data.append(data)

    return JsonResponse(subscriptions_data, safe=False)

@csrf_exempt
def AddHospitalsByAPI(request):
    error_msgs = []
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        number = request.POST.get('number')
        address = request.POST.get('address')
        lang = request.POST.get('lang')
        subscription_id = request.POST.get('subscription_id')
        subscription_scope = request.POST.get('subscription_scope')
        subscription = SubscriptionsModel.objects.get(id=subscription_id)
        users = User.objects.filter(username=username)
        if not users.exists():
            hospital = HospitalsModel.objects.create()
            hospital.name = name
            hospital.number = number
            hospital.address = address
            hospital.lang = lang

            user = User.objects.create(first_name=first_name, last_name=last_name, username=username)
            user.set_password(password)

            userprofile = UserProfile.objects.create(user=user, hospital_profile=hospital, profile_type='0')
            price = None
            if subscription_scope == '1':
                price = subscription.price_monthly
            elif subscription_scope == '2':
                price = subscription.price_yearly
            user_subscription = UserSubscriptionModel.objects.create(subscription=subscription, plan_scope=subscription_scope, price=price)


            user_subscription.save()
            hospital.subscription = user_subscription
            hospital.save()
            user.save()
            userprofile.save()
            os.mkdir(BASE_DIR / f'media/manager/{hospital.id}')

            return JsonResponse({'status':True, 'user_id':user.id, 'user_subscription_id':user_subscription.id}, safe=False)
        else:
            error_msgs.append('يوجد اسم مستخدم من قبل بنفس الاسم')
    return JsonResponse({'status':False, 'msgs':error_msgs}, safe=False)

@csrf_exempt
def RenewSubscription(request, user_id):
    user = User.objects.get(id=user_id)
    hospital = HospitalsModel.objects.get(id=user.userprofile.hospital_profile.id)

    error_msgs = []
    if request.method == 'POST':
        subscription_id = request.POST.get('subscription_id')
        subscription_scope = request.POST.get('subscription_scope')
        subscription = SubscriptionsModel.objects.get(id=subscription_id)

        price = None
        if subscription_scope == '1':
            price = subscription.price_monthly
        elif subscription_scope == '2':
            price = subscription.price_yearly
        user_subscription = UserSubscriptionModel.objects.create(subscription=subscription, plan_scope=subscription_scope, price=price)


        user_subscription.save()
        hospital.subscription = user_subscription
        hospital.save()
        return JsonResponse({'status':True, 'user_id':user.id, 'user_subscription_id':user_subscription.id}, safe=False)

    return JsonResponse({'status':False, 'msgs':error_msgs}, safe=False)

from decimal import Decimal
def GetPatientManagementInfo(request, id):
    user = User.objects.get(id=id)
    hospital_profile = user.userprofile.hospital_profile
    subscription = hospital_profile.subscription

    patients = UserProfile.objects.filter(profile_type='3', hospital_profile=hospital_profile).count()
    managers = UserProfile.objects.filter(Q(profile_type='2', hospital_profile=hospital_profile) | Q(profile_type='0', hospital_profile=hospital_profile)).count()
    patient_vistor = PatientVistorModel.objects.filter(user__userprofile__hospital_profile=hospital_profile)
    patient_medical_report = PatientMedicalReportModel.objects.filter(vistor__user__userprofile__hospital_profile=hospital_profile)


    local_visits = patient_vistor.filter(is_home_visit=False).count()
    home_visits = patient_vistor.filter(is_home_visit=True).count()
    total_visits = patient_vistor.count()

    local_money = Decimal(0)
    home_money = Decimal(0)
    for i in patient_vistor:
        if i.is_home_visit == False:
            local_money += i.visitor_pay_amount
        elif i.is_home_visit == True:
            home_money += i.visitor_pay_amount

    data = {
        'username':user.username,
        'hospital_name': hospital_profile.name,
        'lang': hospital_profile.get_lang_display(),
        'patients':patients,
        'managers':managers,
        'total_visits':total_visits,
        'local_visits':local_visits,
        'home_visits':home_visits,
        'patient_medical_report':patient_medical_report.count(),
        'local_money':local_money,
        'home_money':home_money,
        'subscription':{
            'title': subscription.subscription.title,
            'price': float(subscription.price),
            'plan_scope': subscription.get_plan_scope_display(),
            'plan_scope_id': subscription.plan_scope,
            'creation_date': (subscription.creation_date.strftime("%Y-%m-%d")),
            'end_date': hospital_profile.subscription_end_date(),
            'has_subscription':hospital_profile.is_has_subscription(),
        },
    }
    print(data['subscription'])

    return JsonResponse(data, safe=False)



def DeletePatientManagementAPI(request, id):
    user = User.objects.get(id=id)
    hospital_profile = HospitalsModel.objects.get(id=user.userprofile.hospital_profile.id)
    userprofiles = UserProfile.objects.filter(hospital_profile=hospital_profile)
    for userprofile in userprofiles:
        user = User.objects.get(id=userprofile.user.id)
        user.delete()
    hospital_profile.delete()

    return JsonResponse({'status':True}, safe=False)

@csrf_exempt
def ResetPasswordAPI(request, id):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = User.objects.get(id=id)
        user.set_password(password)
        return JsonResponse({'status':True}, safe=False)
    return JsonResponse({'status':False}, safe=False)