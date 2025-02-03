from accounts.models import PatientVistorModel, PatientMedicalReportModel, UserProfile, CustomizeMedicalTestsModel, HospitalsModel
from .models import MedicalTestsModel
from django.contrib.auth.models import User
from django.db.models import Q
import shutil
from django.conf import settings
from pathlib import Path

BASE_DIR = settings.BASE_DIR


def get_hospital(user):
    hospital = HospitalsModel.objects.filter(id=user.userprofile.hospital_profile.id)
    if hospital.exists():
        return hospital.first()
    return None


def number_of_patient_rule(user):
    hospital_profile = get_hospital(user)
    subscription = hospital_profile.subscription
    if hospital_profile and subscription:
        userprofiles = UserProfile.objects.filter(profile_type='3', hospital_profile=hospital_profile).order_by('-id')
        number_of_patient = subscription.subscription.number_of_patient
        if userprofiles.count() < number_of_patient:
            return True
    return False


def number_of_local_visit_rule(user):
    hospital_profile = get_hospital(user)
    subscription = hospital_profile.subscription
    if hospital_profile and subscription:
        vistors = PatientVistorModel.objects.filter(is_home_visit=False, user__userprofile__hospital_profile=hospital_profile).order_by('-id')
        number_of_local_visit = subscription.subscription.number_of_local_visit
        if vistors.count() < number_of_local_visit:
            return True
    return False

def number_of_home_visit_rule(user):
    hospital_profile = get_hospital(user)
    subscription = hospital_profile.subscription
    if hospital_profile and subscription:
        vistors = PatientVistorModel.objects.filter(is_home_visit=True, user__userprofile__hospital_profile=hospital_profile).order_by('-id')
        number_of_home_visit = subscription.subscription.number_of_home_visit
        if vistors.count() < number_of_home_visit:
            return True
    return False

def number_of_visit_medical_reports_rule(user):
    hospital_profile = get_hospital(user)
    subscription = hospital_profile.subscription
    if hospital_profile and subscription:
        reports = PatientMedicalReportModel.objects.filter(vistor__user__userprofile__hospital_profile=hospital_profile).order_by('-id')
        number_of_visit_medical_reports = subscription.subscription.number_of_visit_medical_reports
        if reports.count() < number_of_visit_medical_reports:
            return True
    return False

def number_of_customize_medical_tests_rule(user):
    hospital_profile = get_hospital(user)
    subscription = hospital_profile.subscription
    if hospital_profile and subscription:
        medical_tests = CustomizeMedicalTestsModel.objects.filter(hospital_profile=hospital_profile).order_by('-id')
        number_of_customize_medical_tests = subscription.subscription.number_of_customize_medical_tests
        if medical_tests.count() < number_of_customize_medical_tests:
            return True
    return False


def number_of_medical_tests_reports_rule(user):
    hospital_profile = get_hospital(user)
    subscription = hospital_profile.subscription
    if hospital_profile and subscription:
        medical_tests = MedicalTestsModel.objects.filter(patient__userprofile__hospital_profile=hospital_profile).order_by('-id')
        number_of_medical_tests_reports = subscription.subscription.number_of_medical_tests_reports
        if medical_tests.count() < number_of_medical_tests_reports:
            return True
    return False

def number_of_manager_rule(user):
    hospital_profile = get_hospital(user)
    subscription = hospital_profile.subscription
    if hospital_profile and subscription:
        users = User.objects.filter(Q(userprofile__profile_type='0', userprofile__hospital_profile=hospital_profile) | Q(userprofile__profile_type='2', userprofile__hospital_profile=hospital_profile))
        number_of_manager = subscription.subscription.number_of_manager
        print(users)
        if users.count() < number_of_manager:
            return True
    return False


def get_hospital_disk_info(user):
    hospital_profile = get_hospital(user)
    path = BASE_DIR / f'media/manager/{hospital_profile.id}/'
    try:

        root_directory = Path(path)
        used = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
        return {'used':used}
    except:
        return {'used':0}
    
def hosptial_storage_size_mb_rule(user, files_size):
    hospital_profile = get_hospital(user)
    subscription = hospital_profile.subscription
    if hospital_profile and subscription:
        hosptial_storage_size_mb = subscription.subscription.hosptial_storage_size_mb
        disk_info = get_hospital_disk_info(user)
        used = disk_info.get('used', 0)

        used_mb = used/(1024*1024)
        files_size_mb = files_size/(1024*1024)

        total_used = files_size_mb + used_mb
        if total_used < hosptial_storage_size_mb:
            return True
    return False