from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserProfile, CompanyRandomNumCodeGen, PatientVistorModel, PatientMedicalReportModel, visit_distance_choices, CustomizeMedicalTestsModel, HospitalsModel
from accounts.fields import GenderFields
import datetime, json, pdfkit
from django.utils import timezone
from django.conf import settings
from decimal import Decimal
from .libs import medical_tests_html_to_dict, medical_test_scraper, ModelToDoc, get_general_settings
from .models import MedicalTestsModel, UploadImageModel, AdminPermissionModel
from django.template.loader import render_to_string
from django.http import FileResponse
from .forms import AdminPermissionModelForm, UserProfileModelForm, UserModelForm
from admin_panel.forms import HospitalsModelForm
from django.db.models import Q
import base64, os
from io import BytesIO
from  PIL import Image
from django.utils import translation
from pathlib import Path
from .subscription_rules import number_of_patient_rule, number_of_local_visit_rule, number_of_home_visit_rule, number_of_customize_medical_tests_rule, number_of_medical_tests_reports_rule, number_of_visit_medical_reports_rule, number_of_manager_rule
from django.contrib import messages
# Create your views here.
BASE_DIR = settings.BASE_DIR

def img_to_base64(file):
    file_format = Path(file.name).suffix
    image = Image.open(file)
    buffered = BytesIO(file.read())
    if image.mode in ("RGBA", "P"):
        bg = Image.new("RGBA", image.size, (255,255,255))
        image = Image.alpha_composite(bg, image)
        image = image.convert('RGB')

    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode()


def PanelHome(request):
    hospital_profile = request.user.userprofile.hospital_profile
    patient_vistor = PatientVistorModel.objects.filter(user__userprofile__hospital_profile=hospital_profile)
    patient_medical_report = PatientMedicalReportModel.objects.filter(vistor__user__userprofile__hospital_profile=hospital_profile)
    # userprofiles = UserProfile.objects.filter().order_by('-id')
    # byte = ModelToDoc(models=userprofiles, fields=['user__username', 'user__first_name', 'phone'])
    # print(byte)
    datetime_now = timezone.now()
    #visitors_count_by_day
    viewsers_count_days = request.GET.get('viewsers_count_days')
    analatic_count_days = request.GET.get('analatic_count_days')
    announced_count_days = request.GET.get('announced_count_days')

    if viewsers_count_days:viewsers_count_days = int(viewsers_count_days)
    else:viewsers_count_days=7
    if announced_count_days:announced_count_days = int(announced_count_days)
    else:announced_count_days=7
    if analatic_count_days:analatic_count_days = int(analatic_count_days)
    else:analatic_count_days=1

        
    viewsers_count_by_day = []
    viewsers_count_by_day2 = []
    for i in range(0, viewsers_count_days):
        i = datetime.datetime.now() + datetime.timedelta(days=-i)
        companys_count = patient_vistor.filter(creation_date__year=i.year, creation_date__month=i.month, creation_date__day=i.day, is_home_visit=False).count()
        companys_count2 = patient_vistor.filter(creation_date__year=i.year, creation_date__month=i.month, creation_date__day=i.day, is_home_visit=True).count()
        viewsers_count_by_day.append((i.date, companys_count))
        viewsers_count_by_day2.append((i.date, companys_count2))


    #reports

    announced_count_by_day = []
    presenters_count_by_day = []
    for i in range(0, announced_count_days):
        i = datetime.datetime.now() + datetime.timedelta(days=-i)
        companys_count = patient_medical_report.filter(creation_date__year=i.year, creation_date__month=i.month, creation_date__day=i.day, vistor__is_home_visit=False).count()
        companys_count2 = patient_medical_report.filter(creation_date__year=i.year, creation_date__month=i.month, creation_date__day=i.day, vistor__is_home_visit=True).count()

        announced_count_by_day.append((i.date, companys_count))
        presenters_count_by_day.append((i.date, companys_count2))


    today_patient = 0
    today_local_patient = 0
    today_home_patient = 0
    today_reports = 0

    today_money = Decimal(0)
    today_local_money = Decimal(0)
    today_home_money = Decimal(0)
    today_km_money = [0, 0]

    for i in range(0, analatic_count_days):
        i = datetime_now + datetime.timedelta(days=-i)

        today_patient += UserProfile.objects.filter(creation_date__date=i.date(), profile_type='3', hospital_profile=hospital_profile).count()
        today_local_patient += patient_vistor.filter(creation_date__date=i.date(), is_home_visit=False).count()
        today_home_patient += patient_vistor.filter(creation_date__date=i.date(), is_home_visit=True).count()
        today_reports += patient_medical_report.filter(creation_date__date=i.date()).count()



        for i in patient_vistor.filter(creation_date__date=i.date()):
            today_money += i.visitor_pay_amount
            if i.is_home_visit == False:
                today_local_money += i.visitor_pay_amount
            elif i.is_home_visit == True:
                today_home_money += i.visitor_pay_amount
                if i.visit_distance == '1':
                    today_km_money[0] = today_km_money[0] + 1
                elif i.visit_distance == '2':
                    today_km_money[1] = today_km_money[1] + 1
    obj = {
        'viewsers_count_days':viewsers_count_days,
        'announced_count_days':announced_count_days,
        'viewsers_count_by_day':viewsers_count_by_day,
        'analatic_count_days':analatic_count_days,
        'viewsers_count_by_day2':viewsers_count_by_day2,
        'announced_count_by_day':announced_count_by_day,
        'presenters_count_by_day':presenters_count_by_day,
        'today_patient':today_patient,
        'today_local_patient':today_local_patient,
        'today_home_patient':today_home_patient,
        'today_reports':today_reports,
        'today_money': today_money,
        'today_local_money': today_local_money,
        'today_home_money': today_home_money,
        'today_km_money': today_km_money,
    }
    return render(request, 'panel/panel.html', obj)

def ManagePatients(request):
    hospital_profile = request.user.userprofile.hospital_profile
    userprofiles = UserProfile.objects.filter(profile_type='3', hospital_profile=hospital_profile).order_by('-id')

    first_name = request.GET.get('first_name')
    if first_name:userprofiles = userprofiles.filter(user__first_name__contains=first_name)
    else:first_name=''
    
    last_name = request.GET.get('last_name')
    if last_name:userprofiles = userprofiles.filter(user__last_name__contains=last_name)
    else:last_name=''

    gender = request.GET.get('gender')
    if gender:userprofiles = userprofiles.filter(gender=gender)
    else:gender=''

    id_number = request.GET.get('id_number')
    if id_number:userprofiles = userprofiles.filter(id_number__contains=id_number)
    else:id_number=''

    search_email = request.GET.get('search_email')
    if search_email:userprofiles = userprofiles.filter(user__email=search_email)
    else:search_email=''

    search_phone = request.GET.get('search_phone')
    if search_phone:userprofiles = userprofiles.filter(phone=search_phone)
    else:search_phone=''

    publish_date = request.GET.get('publish_date')
    if publish_date:userprofiles = userprofiles.filter(creation_date__date=datetime.datetime.strptime(publish_date, '%Y-%m-%d'))
    else:publish_date=''

    
    fields = {
        'first_name':first_name,
        'last_name':last_name,
        'id_number':id_number,
        'gender':gender,
        'publish_date':publish_date,
        'search_email':search_email,
        'search_phone':search_phone,
        'userprofiles':userprofiles,
        'GenderFields':GenderFields,
        'hospital_profile':hospital_profile,
    }

    return render(request, 'panel/Patients/PanelShowPatients.html', fields)

def AddPatients(request):
    add_patient_rule = number_of_patient_rule(request.user)
    if add_patient_rule:
            
        hospital_profile = request.user.userprofile.hospital_profile
        if request.method == 'POST':
            userprofiles = UserProfile.objects.filter(profile_type='3').order_by('-id')
            username = CompanyRandomNumCodeGen()
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            id_number = request.POST.get('id_number')
            gender = request.POST.get('gender')
            birth_date = request.POST.get('birth_date')
            addVisit = request.POST.get('addVisit')
            birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d').date()

            if userprofiles.filter(id_number=id_number, hospital_profile=hospital_profile).exists():
                messages.error(request, 'المريض موجود بالفعل.')
                return redirect(reverse('ManagePatients')+f'?id_number={id_number}')

            user = User.objects.create(username=username, first_name=first_name, last_name=last_name)
            userprofile = UserProfile.objects.create(user=user, profile_type='3', phone=phone, gender=gender, birth_date=birth_date, address=address, id_number=id_number, hospital_profile=hospital_profile)
            user.save()
            userprofile.save()

            hospital_profile_path = BASE_DIR / f'media/manager/{hospital_profile.id}'
            if not os.path.exists(hospital_profile_path):
                os.mkdir(hospital_profile_path)
            os.mkdir(BASE_DIR / f'media/manager/{hospital_profile.id}/{user.id}')
            
            if addVisit == '1':
                return redirect(reverse('AddPatientVisit')+f'?patient_id={user.id}')
            elif addVisit == '2':
                return redirect(reverse('AddPatientHomeVisit')+f'?patient_id={user.id}')
            
            return redirect('ManagePatients')
        return render(request, 'panel/Patients/AddPatients.html', {'GenderFields':GenderFields})
    else:
        messages.error(request, 'تم الوصول الى الحد الاقصى من عدد اضافة المرضى يرجى ترقية الباقة')
        return redirect('ManagePatients')

def EditPatients(request, id):
    user = User.objects.get(id=id)
    userprofile = UserProfile.objects.get(user=user)
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    phone = userprofile.phone
    address = userprofile.address
    id_number = userprofile.id_number
    gender = userprofile.gender
    birth_date = userprofile.birth_date
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        id_number = request.POST.get('id_number')
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth_date')
        birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d').date()

        user.first_name = first_name
        user.last_name = last_name
        # user.email = email
        userprofile.phone = phone
        userprofile.address = address
        userprofile.id_number = id_number
        userprofile.gender = gender
        userprofile.birth_date = birth_date
        user.save()
        userprofile.save()
        return redirect('ManagePatients')
    obj = {
    "userprofile": userprofile,
    "username": username,
    "first_name": first_name,
    "last_name": last_name,
    "email": email,
    "phone": phone,
    "address": address,
    "id_number": id_number,
    "gender": gender,
    "birth_date": str(birth_date),
    'GenderFields': GenderFields
    }
    return render(request, 'panel/Patients/EditPatients.html', obj)

def DeletePatient(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('ManagePatients')






def ManagePatientVisits(request):
    hospital_profile = request.user.userprofile.hospital_profile
    vistors = PatientVistorModel.objects.filter(is_home_visit=False, user__userprofile__hospital_profile=hospital_profile).order_by('-id')

    first_name = request.GET.get('first_name')
    if first_name:vistors = vistors.filter(user__first_name__contains=first_name)
    else:first_name=''
    
    last_name = request.GET.get('last_name')
    if last_name:vistors = vistors.filter(user__last_name__contains=last_name)
    else:last_name=''

    gender = request.GET.get('gender')
    if gender:vistors = vistors.filter(user__userprofile__gender=gender)
    else:gender=''

    id_number = request.GET.get('id_number')
    if id_number:vistors = vistors.filter(user__userprofile__id_number__contains=id_number)
    else:id_number=''

    search_email = request.GET.get('search_email')
    if search_email:vistors = vistors.filter(user__email=search_email)
    else:search_email=''

    search_phone = request.GET.get('search_phone')
    if search_phone:vistors = vistors.filter(user__userprofile__phone=search_phone)
    else:search_phone=''

    publish_date = request.GET.get('publish_date')
    if publish_date:vistors = vistors.filter(creation_date__date=datetime.datetime.strptime(publish_date, '%Y-%m-%d'))
    else:publish_date=''


    fields = {
        'first_name':first_name,
        'last_name':last_name,
        'id_number':id_number,
        'gender':gender,
        'publish_date':publish_date,
        'search_email':search_email,
        'search_phone':search_phone,
        'vistors':vistors,
        'GenderFields':GenderFields,
    }

    return render(request, 'panel/Visits/Normal/ManagePatientVisits.html', fields)


def AddPatientVisit(request):
    if number_of_local_visit_rule(request.user):
            
        hospital_profile = request.user.userprofile.hospital_profile
        patients = UserProfile.objects.filter(profile_type='3', hospital_profile=hospital_profile)
        patient_id = request.GET.get('patient_id')
        if request.method == 'POST':
            patient_user = request.POST.get('patient_user')
            if patient_id:
                patient_user=patient_id
            visitor_pay_amount = request.POST.get('visitor_pay_amount')
            if visitor_pay_amount:
                visitor_pay_amount = Decimal(visitor_pay_amount)

            note = request.POST.get('note')

            user = User.objects.get(id=patient_user)
            vist = PatientVistorModel.objects.create(user=user, note=note, visitor_pay_amount=visitor_pay_amount, creation_date=timezone.now())
            vist.save()
            return redirect('AddMedicalReport', vist.id)
            # return redirect('ManagePatientVisits')
        return render(request, 'panel/Visits/Normal/AddPatientVisit.html', {'GenderFields':GenderFields, 'patients':patients, 'patient_id':patient_id})
    else:
        messages.error(request, 'تم الوصول الى الحد الاقصى من عدد اضافة الزيارات المحلية يرجى ترقية الباقة')
        return redirect('ManagePatientVisits')

def EditPatientVisit(request, id):
    patient = PatientVistorModel.objects.get(id=id)
    patient_user = patient.user.id
    visitor_pay_amount = patient.visitor_pay_amount
    note = patient.note
    patients = UserProfile.objects.filter(profile_type='3')
    if request.method == 'POST':
        patient_user = request.POST.get('patient_user')
        visitor_pay_amount = request.POST.get('visitor_pay_amount')
        if visitor_pay_amount:
            visitor_pay_amount = Decimal(visitor_pay_amount)

        note = request.POST.get('note')
        user = User.objects.get(id=patient_user)
        vist = PatientVistorModel.objects.get(id=id)
        vist.user= user
        vist.note=note
        vist.visitor_pay_amount=visitor_pay_amount
        vist.save()
        return redirect('ManagePatientVisits')
    return render(request, 'panel/Visits/Normal/EditPatientVisit.html', {'GenderFields':GenderFields, 'patients':patients, 'patient_user':patient_user, 'visitor_pay_amount':str(visitor_pay_amount), 'note':note})

def DeletePatientVisit(request, id):
    user = PatientVistorModel.objects.get(id=id)
    user.delete()
    return redirect('ManagePatientVisits')


def PayPatientNormalVisit(request, id):
    user = PatientVistorModel.objects.get(id=id)
    if request.method == 'POST':
        visitor_pay_amount = request.POST.get('visitor_pay_amount', '0').replace(',', '.')
        
        user.visitor_pay_amount = Decimal(visitor_pay_amount)
        user.save()
    return redirect('ManagePatientVisits')


def PayPatientHomeVisit(request, id):
    user = PatientVistorModel.objects.get(id=id)
    if request.method == 'POST':
        visitor_pay_amount = request.POST.get('visitor_pay_amount', '0').replace(',', '.')
        user.visitor_pay_amount = Decimal(visitor_pay_amount)
        user.save()
    return redirect('ManagePatientHomeVisits')

def AddMedicalReport(request, id):
    if number_of_visit_medical_reports_rule(request.user):
            
        visit = PatientVistorModel.objects.get(id=id)
        hospital_profile = request.user.userprofile.hospital_profile
        doctors = UserProfile.objects.filter(profile_type = '2', hospital_profile=hospital_profile)
        file = open(str(BASE_DIR / 'accounts/diagnosis_codes3.json'), 'r').read()
        diagnosises = json.loads(file)

        if request.method == 'POST':
            doctor_user = request.POST.get('doctor_user')
            reason_for_visit = request.POST.get('reason_for_visit')
            clinical_examination = request.POST.get('clinical_examination')
            treatment = request.POST.get('treatment')
            diagnosis = request.POST.get('diagnosis')
            is_custom_diagnosis = request.POST.get('is_custom_diagnosis')
            custom_diagnosis = request.POST.get('custom_diagnosis')
            recommendations = request.POST.get('recommendations')
            
            pulse = request.POST.get('pulse')
            pressure = request.POST.get('pressure')
            oxygen = request.POST.get('oxygen')
            sugar = request.POST.get('sugar')

            
            doctor = User.objects.get(id=doctor_user)
            report = PatientMedicalReportModel.objects.create(vistor=visit, doctor=doctor, recommendations=recommendations, treatment=treatment, reason_for_visit=reason_for_visit, clinical_examination=clinical_examination, creation_date=timezone.now(), pulse=pulse, pressure=pressure, oxygen=oxygen, sugar=sugar)
            if is_custom_diagnosis:
                report.is_custom_diagnosis = True
                report.custom_diagnosis = custom_diagnosis
            else:
                report.is_custom_diagnosis = False
                report.diagnosis = diagnosis

            report.save()
            return redirect('ManageVisitMedicalReport', visit.id)
        return render(request, 'panel/Visits/Reports/MedicalReport/AddMedicalReport.html', {'GenderFields':GenderFields, 'visit':visit, 'doctors':doctors, 'diagnosises':diagnosises})
    else:
        messages.error(request, 'تم الوصول الى الحد الاقصى من عدد اضافة التقارير الطبية يرجى ترقية الباقة')
        return redirect('ManageVisitMedicalReport', id)


def EditMedicalReport(request, id):
    report = PatientMedicalReportModel.objects.get(id=id)
    vistor = report.vistor
    doctors = UserProfile.objects.filter(profile_type = '2')
    doctor = report.doctor
    reason_for_visit = report.reason_for_visit
    clinical_examination = report.clinical_examination
    treatment = report.treatment
    diagnosis_code = report.diagnosis
    recommendations = report.recommendations

    pulse = report.pulse
    pressure = report.pressure
    oxygen = report.oxygen
    sugar = report.sugar

    file = open(str(BASE_DIR / 'accounts/diagnosis_codes3.json'), 'r').read()
    diagnosises = json.loads(file)

    if request.method == 'POST':
        doctor_user = request.POST.get('doctor_user')
        reason_for_visit = request.POST.get('reason_for_visit')
        clinical_examination = request.POST.get('clinical_examination')
        treatment = request.POST.get('treatment')
        diagnosis = request.POST.get('diagnosis')
        is_custom_diagnosis = request.POST.get('is_custom_diagnosis')
        custom_diagnosis = request.POST.get('custom_diagnosis')
        recommendations = request.POST.get('recommendations')
        
        pulse = request.POST.get('pulse')
        pressure = request.POST.get('pressure')
        oxygen = request.POST.get('oxygen')
        sugar = request.POST.get('sugar')

        doctor = User.objects.get(id=doctor_user)
        report.doctor=doctor
        report.recommendations=recommendations
        report.treatment=treatment
        report.reason_for_visit=reason_for_visit
        report.clinical_examination=clinical_examination

        if is_custom_diagnosis:
            report.is_custom_diagnosis = True
            report.custom_diagnosis = custom_diagnosis
        else:
            report.is_custom_diagnosis = False
            report.diagnosis = diagnosis

        report.pulse = pulse
        report.pressure = pressure
        report.oxygen = oxygen
        report.sugar = sugar

        report.save()
        return redirect('ManageVisitMedicalReport', vistor.id)
    obj = {
        'report':report,
        'visit':vistor,
        'doctor': doctor,
        'reason_for_visit': reason_for_visit,
        'clinical_examination': clinical_examination,
        'treatment': treatment,
        'diagnosis_code': diagnosis_code,
        'recommendations': recommendations,
        'pulse': pulse,
        'pressure': pressure,
        'oxygen': oxygen,
        'sugar': sugar,

        'GenderFields':GenderFields, 'doctors':doctors, 'diagnosises':diagnosises}
    return render(request, 'panel/Visits/Reports/MedicalReport/EditMedicalReport.html', obj)




def ViewMedicalReport(request, id):
    report = PatientMedicalReportModel.objects.get(id=id)
    vistor = report.vistor
    doctors = UserProfile.objects.filter(profile_type = '2')
    doctor = report.doctor
    reason_for_visit = report.reason_for_visit
    clinical_examination = report.clinical_examination
    treatment = report.treatment
    diagnosis_code = report.diagnosis
    recommendations = report.recommendations

    pulse = report.pulse
    pressure = report.pressure
    oxygen = report.oxygen
    sugar = report.sugar

    file = open(str(BASE_DIR / 'accounts/diagnosis_codes3.json'), 'r').read()
    diagnosises = json.loads(file)

    obj = {
        'report':report,
        'visit':vistor,
        'doctor': doctor,
        'reason_for_visit': reason_for_visit,
        'clinical_examination': clinical_examination,
        'treatment': treatment,
        'diagnosis_code': diagnosis_code,
        'recommendations': recommendations,
        'pulse': pulse,
        'pressure': pressure,
        'oxygen': oxygen,
        'sugar': sugar,

        'GenderFields':GenderFields, 'doctors':doctors, 'diagnosises':diagnosises}
    return render(request, 'panel/Visits/Reports/MedicalReport/ViewMedicalReport.html', obj)




def ManageVisitMedicalReport(request, id):
    visit = PatientVistorModel.objects.get(id=id)
    reports = PatientMedicalReportModel.objects.filter(vistor=visit).order_by('-id')

    return render(request, 'panel/Visits/Reports/MedicalReport/ManageVisitMedicalReport.html', {'GenderFields':GenderFields, 'visit':visit, 'reports':reports})


def DeleteMedicalReport(request, id):
    
    user = PatientMedicalReportModel.objects.get(id=id)
    visit = user.vistor
    user.delete()
    return redirect('ManageVisitMedicalReport', visit.id)




# Home Visit
def ManagePatientHomeVisits(request):
    hospital_profile = request.user.userprofile.hospital_profile
    vistors = PatientVistorModel.objects.filter(is_home_visit=True, user__userprofile__hospital_profile=hospital_profile).order_by('-id')

    first_name = request.GET.get('first_name')
    if first_name:vistors = vistors.filter(user__first_name__contains=first_name)
    else:first_name=''
    
    last_name = request.GET.get('last_name')
    if last_name:vistors = vistors.filter(user__last_name__contains=last_name)
    else:last_name=''

    gender = request.GET.get('gender')
    if gender:vistors = vistors.filter(user__userprofile__gender=gender)
    else:gender=''

    id_number = request.GET.get('id_number')
    if id_number:vistors = vistors.filter(user__userprofile__id_number__contains=id_number)
    else:id_number=''

    search_email = request.GET.get('search_email')
    if search_email:vistors = vistors.filter(user__email=search_email)
    else:search_email=''

    search_phone = request.GET.get('search_phone')
    if search_phone:vistors = vistors.filter(user__userprofile__phone=search_phone)
    else:search_phone=''

    publish_date = request.GET.get('publish_date')
    if publish_date:vistors = vistors.filter(creation_date__date=datetime.datetime.strptime(publish_date, '%Y-%m-%d'))
    else:publish_date=''


    fields = {
        'first_name':first_name,
        'last_name':last_name,
        'id_number':id_number,
        'gender':gender,
        'publish_date':publish_date,
        'search_email':search_email,
        'search_phone':search_phone,
        'vistors':vistors,
        'GenderFields':GenderFields,
    }

    return render(request, 'panel/Visits/Home/ManagePatientHomeVisits.html', fields)


def AddPatientHomeVisit(request):
    if number_of_home_visit_rule(request.user):
            
        hospital_profile = request.user.userprofile.hospital_profile
        patients = UserProfile.objects.filter(profile_type='3', hospital_profile=hospital_profile)
        doctors = UserProfile.objects.filter(profile_type = '2', hospital_profile=hospital_profile)
        patient_id = request.GET.get('patient_id')

        if request.method == 'POST':
            patient_user = request.POST.get('patient_user')
            doctor_user = request.POST.get('doctor_user')
            visitor_pay_amount = request.POST.get('visitor_pay_amount')
            visit_distance = request.POST.get('visit_distance')
            if visitor_pay_amount:
                visitor_pay_amount = Decimal(visitor_pay_amount)

            note = request.POST.get('note')

            user = User.objects.get(id=patient_user)
            doctor = User.objects.get(id=doctor_user)
            vist = PatientVistorModel.objects.create(user=user, doctor=doctor, note=note, is_home_visit=True, visitor_pay_amount=visitor_pay_amount, visit_distance=visit_distance, creation_date=timezone.now())
            vist.save()
            return redirect('ManagePatientHomeVisits')
        return render(request, 'panel/Visits/Home/AddPatientHomeVisit.html', {'GenderFields':GenderFields, 'doctors':doctors, 'patients':patients, 'visit_distance_choices':visit_distance_choices, 'patient_id':patient_id})
    else:
        messages.error(request, 'تم الوصول الى الحد الاقصى من عدد اضافة الزيارات المنزلية يرجى ترقية الباقة')
        return redirect('ManagePatientHomeVisits')

def EditPatientHomeVisit(request, id):
    hospital_profile = request.user.userprofile.hospital_profile
    patient = PatientVistorModel.objects.get(id=id)
    patient_user = patient.user.id
    visitor_pay_amount = patient.visitor_pay_amount
    visit_distance = patient.visit_distance
    doctor_user = patient.doctor.id
    note = patient.note
    patients = UserProfile.objects.filter(profile_type='3', hospital_profile=hospital_profile)
    doctors = UserProfile.objects.filter(profile_type = '2', hospital_profile=hospital_profile)
    
    if request.method == 'POST':
        patient_user = request.POST.get('patient_user')
        doctor_user = request.POST.get('doctor_user')
        visitor_pay_amount = request.POST.get('visitor_pay_amount')
        visit_distance = request.POST.get('visit_distance')
        if visitor_pay_amount:
            visitor_pay_amount = Decimal(visitor_pay_amount)

        note = request.POST.get('note')
        doctor = User.objects.get(id=doctor_user)
        user = User.objects.get(id=patient_user)

        vist = PatientVistorModel.objects.get(id=id)
        vist.user = user
        vist.doctor = doctor
        vist.note = note
        vist.visit_distance = visit_distance
        vist.visitor_pay_amount=visitor_pay_amount
        vist.save()
        return redirect('ManagePatientHomeVisits')
    return render(request, 'panel/Visits/Home/EditPatientHomeVisit.html', {'GenderFields':GenderFields, 'patients':patients, 'patient_user':patient_user, 'visitor_pay_amount':str(visitor_pay_amount), 'note':note, 'doctor_user':doctor_user, 'visit_distance':visit_distance, 'doctors':doctors, 'visit_distance_choices':visit_distance_choices})

def DeletePatientHomeVisit(request, id):
    user = PatientVistorModel.objects.get(id=id)
    user.delete()
    return redirect('ManagePatientHomeVisits')


def ManageCustomizeMedicalTests(request):
    hospital_profile = request.user.userprofile.hospital_profile
    medical_tests = CustomizeMedicalTestsModel.objects.filter(hospital_profile=hospital_profile).order_by('-id')
    return render(request, 'panel/CustomizeMedicalTests/ManageCustomizeMedicalTests.html', {'medical_tests':medical_tests})

def AddCustomizeMedicalTests(request):
    if number_of_customize_medical_tests_rule(request.user):
            
        hospital_profile = request.user.userprofile.hospital_profile
        if request.method == 'POST':
            name = request.POST.get('name')
            medical_test = CustomizeMedicalTestsModel.objects.create(name=name)
            data = medical_tests_html_to_dict(request.POST)
            medical_test.data = data
            medical_test.hospital_profile = hospital_profile
            medical_test.creation_date = timezone.now()
            medical_test.save()
            return redirect('ManageCustomizeMedicalTests')
        # open('accounts/test.html', 'w', encoding="UTF-8").write(request.POST.get('form-box-content'))
        return render(request, 'panel/CustomizeMedicalTests/AddCustomizeMedicalTests.html')
    else:
        messages.error(request, 'تم الوصول الى الحد الاقصى من عدد اضافة تخصيص الفحوصات الطبية يرجى ترقية الباقة')
        return redirect('ManageCustomizeMedicalTests')
    
def EditCustomizeMedicalTests(request, id):
    medical_test = CustomizeMedicalTestsModel.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        data = medical_tests_html_to_dict(request.POST)
        medical_test.name = name
        medical_test.data = data
        medical_test.save()
        messages.success(request, 'تم التعديل بنجاح')
        return redirect('ManageCustomizeMedicalTests')
    return render(request, 'panel/CustomizeMedicalTests/EditCustomizeMedicalTests.html', {'medical_test':medical_test})


def DeleteCustomizeMedicalTests(request, id):
    medical_test = CustomizeMedicalTestsModel.objects.get(id=id)
    medical_test.delete()
    return redirect('ManageCustomizeMedicalTests')


def MedicalTestsManagePatients(request):
    hospital_profile = request.user.userprofile.hospital_profile
    medical_tests = CustomizeMedicalTestsModel.objects.filter(hospital_profile=hospital_profile).order_by('-id')
    userprofiles = UserProfile.objects.filter(profile_type='3', hospital_profile=hospital_profile).order_by('-id')

    first_name = request.GET.get('first_name')
    if first_name:userprofiles = userprofiles.filter(user__first_name__contains=first_name)
    else:first_name=''
    
    last_name = request.GET.get('last_name')
    if last_name:userprofiles = userprofiles.filter(user__last_name__contains=last_name)
    else:last_name=''

    gender = request.GET.get('gender')
    if gender:userprofiles = userprofiles.filter(gender=gender)
    else:gender=''

    id_number = request.GET.get('id_number')
    if id_number:userprofiles = userprofiles.filter(id_number__contains=id_number)
    else:id_number=''

    search_email = request.GET.get('search_email')
    if search_email:userprofiles = userprofiles.filter(user__email=search_email)
    else:search_email=''

    search_phone = request.GET.get('search_phone')
    if search_phone:userprofiles = userprofiles.filter(phone=search_phone)
    else:search_phone=''

    publish_date = request.GET.get('publish_date')
    if publish_date:userprofiles = userprofiles.filter(creation_date__date=datetime.datetime.strptime(publish_date, '%Y-%m-%d'))
    else:publish_date=''


    fields = {
        'first_name':first_name,
        'last_name':last_name,
        'id_number':id_number,
        'gender':gender,
        'publish_date':publish_date,
        'search_email':search_email,
        'search_phone':search_phone,
        'userprofiles':userprofiles,
        'GenderFields':GenderFields,
        'medical_tests':medical_tests,
    }

    return render(request, 'panel/MedicalTests/users/PanelShowPatients.html', fields)


def ManageMedicalTests(request, patient_id):
    hospital_profile = request.user.userprofile.hospital_profile
    patient = User.objects.get(id=patient_id)
    custom_medical_tests = CustomizeMedicalTestsModel.objects.filter(hospital_profile=hospital_profile).order_by('-id')
    medical_tests = MedicalTestsModel.objects.filter(patient=patient).order_by('-id')
    return render(request, 'panel/MedicalTests/reports/ManageMedicalTests.html', {'patient':patient, 'custom_medical_tests':custom_medical_tests, 'medical_tests':medical_tests})

def AddMedicalTests(request, patient_id):
    if number_of_medical_tests_reports_rule(request.user):
            
        patient = User.objects.get(id=patient_id)
        doctor = request.user
        hospital_profile = request.user.userprofile.hospital_profile
        doctors = UserProfile.objects.filter(profile_type = '2', hospital_profile=hospital_profile)
        custom_medical_test_id = request.GET.get('custom_medical_test')
        custom_medical_test = CustomizeMedicalTestsModel.objects.get(id=custom_medical_test_id)
        
        if request.method == 'POST':
            doctor_user = request.POST.get('doctor_user')
            doctor = User.objects.get(id=doctor_user)
            
            medical_test = MedicalTestsModel.objects.create(patient=patient, doctor=doctor, name=custom_medical_test.name)
            data = medical_test_scraper(request.POST, custom_medical_test.data)
            medical_test.data=data
            medical_test.creation_date = timezone.now()
            medical_test.save()

            return redirect('ManageMedicalTests', patient_id)
        return render(request, 'panel/MedicalTests/reports/AddMedicalTests.html', {'patient':patient,'custom_medical_test':custom_medical_test, 'doctors':doctors})
    else:
        messages.error(request, 'تم الوصول الى الحد الاقصى من عدد اضافة تقارير الفحوصات الطبية يرجى ترقية الباقة')
        return redirect('ManageMedicalTests', patient_id)

def EditMedicalTests(request, id):
    hospital_profile = request.user.userprofile.hospital_profile
    medical_test = MedicalTestsModel.objects.get(id=id)
    doctors = UserProfile.objects.filter(profile_type = '2', hospital_profile=hospital_profile)
    doctor = medical_test.doctor
    if request.method == 'POST':
        doctor_user = request.POST.get('doctor_user')
        print(doctor_user)
        doctor = User.objects.get(id=doctor_user)
        data = medical_test_scraper(request.POST, medical_test.data)
        medical_test.data = data
        medical_test.doctor = doctor
        medical_test.save()
        messages.success(request, 'تم التعديل بنجاح')
        return redirect('ManageMedicalTests', medical_test.patient.id)
    return render(request, 'panel/MedicalTests/reports/EditMedicalTests.html', {'medical_test':medical_test, 'doctor':doctor, 'doctors':doctors})


def ViewMedicalTests(request, id):
    medical_test = MedicalTestsModel.objects.get(id=id)
    hospital_profile = request.user.userprofile.hospital_profile
    doctors = UserProfile.objects.filter(profile_type = '2', hospital_profile=hospital_profile)
    doctor = medical_test.doctor
    return render(request, 'panel/MedicalTests/reports/ViewMedicalTests.html', {'medical_test':medical_test, 'doctor':doctor, 'doctors':doctors})



def DeleteMedicalTests(request, id):
    user = MedicalTestsModel.objects.get(id=id)
    patient_id = user.patient.id
    user.delete()
    return redirect('ManageMedicalTests', patient_id)




def GeneralSettings(request):
    hospital_profile = HospitalsModel.objects.get(id=request.user.userprofile.hospital_profile.id)
    form = HospitalsModelForm(instance=hospital_profile)
    if request.method == 'POST':
        form = HospitalsModelForm(data=request.POST, files=request.FILES, instance=hospital_profile)
        if form.is_valid():
            hospital_profile = form.save(commit=False)
            if hospital_profile.img:
                img_base64 = img_to_base64(hospital_profile.img.open('rb'))
                hospital_profile.img_base64 = img_base64
            hospital_profile.save()
            translation.activate(hospital_profile.lang)
            return redirect('GeneralSettings')

    return render(request, 'panel/settings/general/edit.html', {'form':form, 'hospital_profile':hospital_profile})


def MedicalReportToPDF(request, id):
    download = request.GET.get('download')
    hospital_profile = HospitalsModel.objects.get(id=request.user.userprofile.hospital_profile.id)

    report = PatientMedicalReportModel.objects.get(id=id)
    rendered = render_to_string('panel/Visits/Reports/MedicalReportPDF/getEmployeeComeDaysDataForAll.html', {'report':report, 'hospital_profile':hospital_profile}, request=request)
    # print(rendered)
    path_wkhtmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
    path_wkhtmltopdf_ub = '/usr/bin/wkhtmltopdf'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    path = f'media/reports/{request.user.username}{request.user.id}.pdf'
    pdfkit.from_string(str(rendered), str(BASE_DIR/path), configuration=config, options={"enable-local-file-access": ""})
    res = FileResponse(open(str(BASE_DIR/path), 'rb'))
    if download:
        res['Content-Disposition'] = f'attachment; filename="{request.user.username}.pdf"'
    return res



def MedicalTestsReportToPDF(request, id):
    download = request.GET.get('download')
    hospital_profile = HospitalsModel.objects.get(id=request.user.userprofile.hospital_profile.id)

    
    report = MedicalTestsModel.objects.get(id=id)
    rendered = render_to_string('panel/MedicalTests/ReportPDF/getEmployeeComeDaysDataForAll.html', {'report':report, 'hospital_profile':hospital_profile}, request=request)
    # print(rendered)
    path_wkhtmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
    path_wkhtmltopdf_ub = '/usr/bin/wkhtmltopdf'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    path = f'media/reports/{request.user.username}{request.user.id}.pdf'
    pdfkit.from_string(str(rendered), str(BASE_DIR/path), configuration=config, options={"enable-local-file-access": ""})
    res = FileResponse(open(str(BASE_DIR/path), 'rb'))
    if download:
        res['Content-Disposition'] = f'attachment; filename="{request.user.username}.pdf"'
    return res


def ManageAdminPermission(request):
    hospital_profile = request.user.userprofile.hospital_profile
    objs = UserProfile.objects.filter(hospital_profile=hospital_profile).filter(Q(profile_type='2'))

    return render(request, 'panel/admin_permission/ManageAdminPermission.html', {'objs':objs})

def AddAdminPermission(request):
    if number_of_manager_rule(request.user):
            
        hospital_profile = request.user.userprofile.hospital_profile

        userprofile_form = UserProfileModelForm()
        user_form = UserModelForm()
        form = AdminPermissionModelForm()
        if request.method == 'POST':
            form = AdminPermissionModelForm(data=request.POST)
            userprofile_form = UserProfileModelForm(data=request.POST)
            user_form = UserModelForm(data=request.POST)
            if form.is_valid() and userprofile_form.is_valid() and user_form.is_valid():
                password = request.POST.get('password')

                user = user_form.save(commit=False)
                if password:
                    user.set_password(password)

                ob = form.save(commit=False)
                ob.creation_date = timezone.now()

                userprofile = userprofile_form.save(commit=False)
                userprofile.user = user
                userprofile.permissions = ob
                userprofile.profile_type = '2'
                userprofile.hospital_profile = hospital_profile

                user.save()
                ob.save()
                userprofile.save()

                return redirect('ManageAdminPermission')
    else:
        messages.error(request, 'تم الوصول الى الحد الاقصى من عدد اضافة المدراء يرجى ترقية الباقة')
        return redirect('ManageAdminPermission')
    
    return render(request, 'panel/admin_permission/AddAdminPermission.html', {'form':form, 'userprofile_form':userprofile_form, 'user_form':user_form})

def EditAdminPermission(request, id):
    userprofile = UserProfile.objects.get(id=id)
    permission = AdminPermissionModel.objects.get(id=userprofile.permissions.id)
    user = User.objects.get(id=userprofile.user.id)

    form = AdminPermissionModelForm(instance=permission)
    userprofile_form = UserProfileModelForm(instance=userprofile)
    user_form = UserModelForm(instance=user)

    if request.method == 'POST':
        form = AdminPermissionModelForm(data=request.POST, instance=permission)
        userprofile_form = UserProfileModelForm(data=request.POST, instance=userprofile)
        user_form = UserModelForm(data=request.POST, instance=user)
        if form.is_valid() and userprofile_form.is_valid() and user_form.is_valid():
            password = request.POST.get('password')

            if password:
                user = user_form.save(commit=False)
                user.set_password(password)
                user.save()
            else:
                user_form.save()

            form.save()
            userprofile_form.save()
            return redirect('ManageAdminPermission')
    return render(request, 'panel/admin_permission/EditAdminPermission.html', {'form':form, 'userprofile_form':userprofile_form, 'user_form':user_form})

def DeleteAdminPermission(request, id):
    userprofile = UserProfile.objects.get(id=id)
    permission = AdminPermissionModel.objects.get(id=userprofile.permissions.id)
    user = User.objects.get(id=userprofile.user.id)
    userprofile.delete()
    permission.delete()
    user.delete()
    return redirect('ManageAdminPermission')




def PatientsSelectedUsers(request):
    hospital_profile = request.user.userprofile.hospital_profile
    subscription = hospital_profile.subscription.subscription
    if subscription.extract_patient_info:
            
        if request.method == 'POST':
            
            user_ids = request.POST.getlist('user_ids')
            userprofiles = UserProfile.objects.filter(profile_type='3', id__in=user_ids, hospital_profile=hospital_profile).order_by('-id')

            method = request.POST.get('method')
            out_format = request.POST.get('out_format')
            if method == 'xlsx':
                if out_format:
                    byte = ModelToDoc(models=userprofiles, fields=['user__first_name', 'user__last_name', 'phone', 'id_number'], rename_fields={'user__first_name':'اسم الاول', 'user__last_name':'اسم الاخير', 'phone':'الهاتف', 'id_number':'رقم الهوية'}, export_format=out_format)
                    # f = open('wr', 'wb')
                    # f.write(byte)
                    # f.close()

                    res = FileResponse(byte)
                    res['Content-Disposition'] = f'attachment; filename="Patients.{out_format}"'
                    return res
            elif method == 'delete':
                for userprofile in userprofiles:userprofile.delete()
                return redirect('ManagePatients')
    else:
        messages.error(request, 'هذه الاجراء ليس ضمن مميزات الاشتراك الخاص بك يرجى ترقية الاشتراك حتى تتمكن من استخدام هذه الميزة')
        return redirect('ManagePatients')