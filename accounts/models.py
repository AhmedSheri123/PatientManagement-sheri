from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .fields import GenderFields
from .libs import DatetimeNow, when_published
from django.conf import settings
from dashboard.models import AdminPermissionModel, UploadImageModel
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from messenger.models import MessengerModel
import random, json, string, datetime

BASE_DIR = settings.BASE_DIR
# Create your models here.

account_type_choices = (
    ('0', _('Admin')),
    ('2', _('Employee')),
    ('3', _('Patient')),
)

languages_choices = settings.LANGUAGES

account_alias_name_choices = (
    ('0', _('Employee')),
    ('2', _('Doctor')),
    ('3', _('Analyst')),
    ('3', _('Reporter')),
)

visit_distance_choices = (
    ('1', '0-30 KM'),
    ('2', '30-60 KM'),
)

SubscriptionsTheemChoices = (
    ('primary', 'primary'),
    ('secondary', 'secondary'),
    ('success', 'success'),
    ('danger', 'danger'),
    ('warning', 'warning'),
    ('info', 'info'),
    ('light', 'light'),
    ('dark', 'dark'),
)

CurrencyChoices = (
    ("SAR", "ريال سعودي"),
    ("USD", "دولار"),
    ("EUR", "يورو"),
)

plan_type_choices = [
    ('premium', 'Premium'),
    ('pro', 'PRO'),
    ('basic', 'Basic'),
]

plan_scope_choices = [
    ('1', 'Monthly'),
    ('2', 'Yearly')
]

def CompanyRandomNumCodeGen():
    N = 5
    res = ''.join(random.choices(string.digits, k=N))
    return 'p' + str(res)

def payOrderCodeGen():
    N = 16
    res = ''.join(random.choices(string.digits, k=N))
    return 'order' + str(res)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    hospital_profile = models.ForeignKey('HospitalsModel', on_delete=models.SET_NULL, null=True, blank=True)
    permissions = models.ForeignKey(AdminPermissionModel, on_delete=models.SET_NULL, null=True, blank=True)

    profile_type = models.CharField(max_length=255, choices = account_type_choices, null=True, blank=True, verbose_name="نوع الملف الشخصي")
    account_alias_name = models.CharField(max_length=255, choices = account_alias_name_choices, null=True, blank=True, verbose_name=_('Profession'))
    
    phone = models.CharField(max_length=255, verbose_name=_('Phone'), null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, choices=GenderFields, null=True, blank=True, verbose_name=_('Gender'))
    id_number = models.IntegerField(null=True, verbose_name=_('ID Number'))
    birth_date = models.DateField(null=True, verbose_name=_('Birth Date'))

    is_active = models.BooleanField(default=False)
    last_active_datetime = models.DateTimeField(null=True, blank=True)

    is_in_chat = models.BooleanField(default=False)
    active_messenger = models.ForeignKey(MessengerModel, on_delete=models.SET_NULL, null=True, blank=True)

    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")

    def __str__(self):
        return self.user.username
    

    

class PatientProfile(models.Model):
    id_number = models.IntegerField(null=True, verbose_name="العمر")
    birth_date = models.DateField(null=True, verbose_name="العمر")
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")
    # def __str__(self):
    #     return self.name

class PatientVistorModel(models.Model):
    user = models.ForeignKey(User, related_name='vistor_patient', null=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='doctor', null=True, on_delete=models.CASCADE)

    visitor_pay_amount = models.DecimalField(max_digits=6, decimal_places=2)
    is_home_visit = models.BooleanField(default=False)
    visit_distance = models.CharField(max_length=254, choices=visit_distance_choices, null=True, blank=True)

    note = models.TextField(null=True)
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")
    # def __str__(self):
    #     return self.name

    def whenpublished(self):
        return when_published(self.creation_date)

class PatientMedicalReportModel(models.Model):
    vistor = models.ForeignKey(PatientVistorModel, related_name='vistor', on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='vistor_doctor', on_delete=models.CASCADE)
    reason_for_visit = models.TextField()

    pulse = models.CharField(max_length=255, blank=True, null=True)
    pressure = models.CharField(max_length=255, blank=True, null=True)
    oxygen = models.CharField(max_length=255, blank=True, null=True)
    sugar = models.CharField(max_length=255, blank=True, null=True)

    clinical_examination = models.TextField()
    treatment = models.TextField()
    diagnosis = models.CharField(max_length=254)
    is_custom_diagnosis = models.BooleanField(default=False)
    custom_diagnosis = models.CharField(max_length=254, blank=True, null=True, default='')


    recommendations = models.TextField()

    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")
    # def __str__(self):
    #     return self.name

    def whenpublished(self):
        return when_published(self.creation_date)
    
    def get_diagnosis(self):
        file = open(str(BASE_DIR / 'accounts/diagnosis_codes3.json'), 'r').read()
        diagnosises = json.loads(file)
        for i in diagnosises:
            if i.get('code') == self.diagnosis:
                return i.get('descr')
        return ''
    
class HospitalsModel(models.Model):
    name = models.CharField(_('Name'), max_length=254, null=True)
    number = models.CharField(_('Phone'), max_length=254, null=True, blank=True)
    address = models.CharField(_('Address'), max_length=254, null=True, blank=True)
    img = models.ImageField(_('Image'), upload_to='img/%Y/%m', null=True, blank=True)
    img_base64 = models.TextField(_('Profession'), null=True, blank=True)
    lang = models.CharField(_('Language'), max_length=254, choices=languages_choices, default='en')
    subscription = models.ForeignKey('UserSubscriptionModel', on_delete=models.SET_NULL, null=True, blank=True)

    
    def is_has_subscription(self):
        datetime_now = timezone.now()
        date_now = datetime_now.date()
        if self.subscription:
            subscription_date = self.subscription.creation_date.date()
            end_date = (datetime.timedelta(days=self.subscription.number_of_days) + subscription_date)
            if date_now < end_date:
                return True
        return False

    def subscription_end_date(self):
        if self.subscription:
            subscription_date = self.subscription.creation_date
            number_of_days = 0
            if self.subscription.plan_scope == '1':
                number_of_days = 30
            elif self.subscription.plan_scope == '2':
                number_of_days = 365
            end_date = (datetime.timedelta(days=number_of_days) + subscription_date).strftime("%Y-%m-%d")
            return end_date
        return ''

class CustomizeMedicalTestsModel(models.Model):
    hospital_profile = models.ForeignKey(HospitalsModel, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=254, null=True)
    data = models.JSONField(null=True)
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")


    def whenpublished(self):
        return when_published(self.creation_date)
    



class SubscriptionsModel(models.Model):
    title = models.CharField(max_length=255, verbose_name='العنوان')
    subtitle = models.TextField(verbose_name='العنوان الفرعي')
    ico = models.ImageField(upload_to='subscription/ico/', blank=True)

    Theem = models.CharField(max_length=255, choices=SubscriptionsTheemChoices, null=True, verbose_name='الثيم')
    plan_type = models.CharField(max_length=255, choices=plan_type_choices, null=True, verbose_name='نو الاشتراك')

    is_default_Subscription = models.BooleanField(default=False, verbose_name='هل هذه الباقة الافتراضية عند التسجيل')

    number_of_days = models.IntegerField(default=30, verbose_name='عدد الأيام')

    set_defult_price = models.BooleanField(default=False, verbose_name='عرض الباقة في الدول الغير مخصصة')
    price_monthly = models.DecimalField(max_digits=6, null=True, decimal_places=2, verbose_name='السعر')
    discont_monthly = models.IntegerField(default=0, null=True, verbose_name='خصم')

    price_yearly = models.DecimalField(max_digits=6, null=True, decimal_places=2, verbose_name='السعر')
    discont_yearly = models.IntegerField(default=0, null=True, verbose_name='خصم')

    currency = models.CharField(max_length=250, choices=CurrencyChoices, default='USD', null=True, verbose_name='العملة')

    number_of_patient = models.IntegerField(default=1, verbose_name='عدد المرضى')
    number_of_local_visit = models.IntegerField(default=1, verbose_name='عدد الزيارات المحلية')
    number_of_home_visit = models.IntegerField(default=1, verbose_name='عدد الزيارات المنزلية')
    hosptial_storage_size_mb = models.IntegerField(default=1, verbose_name='حجم مساحة تخزين المشفى')
    number_of_visit_medical_reports = models.IntegerField(default=1, verbose_name='عدد اضافة التقارير الطبية')
    number_of_customize_medical_tests = models.IntegerField(default=1, verbose_name='عدد نماذج تخصيص التحاليل')
    number_of_medical_tests_reports = models.IntegerField(default=1, verbose_name='عدد تقارير التحاليل')
    number_of_manager = models.IntegerField(default=1, verbose_name='تحديد عدد المدراء')


    one_to_one_chat = models.BooleanField(default=False, verbose_name='دردشة بين المدراء والموظفين')
    extract_patient_info = models.BooleanField(default=False, verbose_name='استخراج بيانات المرضى (excel, csv, html json)')
    live_chat_with_support = models.BooleanField(default=False, verbose_name='دردشة مباشرة مع الدعم الفني')

    is_enabled = models.BooleanField(default=True, verbose_name='هل الاشتراك قابل للشراء')

    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")

    def __str__(self):
        return str(self.title)



class UserSubscriptionModel(models.Model):
    subscription = models.ForeignKey('SubscriptionsModel', on_delete=models.CASCADE)
    number_of_days = models.IntegerField(default=30)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    plan_scope = models.CharField(max_length=254, choices=plan_scope_choices,  null=True)
    currency = models.CharField(max_length=250, choices=CurrencyChoices, default='USD', null=True, verbose_name='العملة')
    
    creation_date = models.DateTimeField(null=True, default=timezone.now, verbose_name="تاريخ الانشاء")
    def __str__(self):
        return str(self.subscription.title)
    


class UserPaymentOrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    subscription = models.ForeignKey(SubscriptionsModel, on_delete=models.SET_NULL, null=True)
    orderID = models.CharField(max_length=250, default=payOrderCodeGen, null=True, verbose_name="الاسم الثلاثي")
    transactionNo = models.CharField(max_length=250, null=True)
    is_buyed = models.BooleanField(default=False)
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")
