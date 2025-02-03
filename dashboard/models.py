from django.db import models
from django.contrib.auth.models import User
from accounts.libs import when_published
from django.utils.translation import gettext_lazy as _
# Create your models here.



class MedicalTestsModel(models.Model):
    patient = models.ForeignKey(User, related_name='patient_test', null=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='doctor_test', null=True, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=254, null=True)
    data = models.JSONField(null=True)
    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")


    def whenpublished(self):
        return when_published(self.creation_date)
    
class UploadImageModel(models.Model):
    img = models.ImageField(upload_to='img/%Y/%m')
    img_base64 = models.TextField()


class AdminPermissionModel(models.Model):
    is_enabled = models.BooleanField(default=True, verbose_name=_('Is the administrator enabled'))
    show_index = models.BooleanField(default=False, verbose_name=_('Manage the main panel'))

    # Administrator Permissions
    show_admin = models.BooleanField(default=False, verbose_name=_('Manage administrators'))
    add_admin = models.BooleanField(default=False, verbose_name=_('Add administrators'))
    delete_admin = models.BooleanField(default=False, verbose_name=_('Delete administrators'))
    edit_admin = models.BooleanField(default=False, verbose_name=_('Edit administrators'))

    # Patient Permissions
    show_patient = models.BooleanField(default=False, verbose_name=_('Manage patients'))
    add_patient = models.BooleanField(default=False, verbose_name=_('Add patient'))
    delete_patient = models.BooleanField(default=False, verbose_name=_('Delete patient'))
    edit_patient = models.BooleanField(default=False, verbose_name=_('Edit patient'))

    # Normal Visit Permissions
    show_normal_visit = models.BooleanField(default=False, verbose_name=_('Manage normal visits'))
    add_normal_visit = models.BooleanField(default=False, verbose_name=_('Add normal visit'))
    delete_normal_visit = models.BooleanField(default=False, verbose_name=_('Delete normal visit'))
    edit_normal_visit = models.BooleanField(default=False, verbose_name=_('Edit normal visit'))

    # Home Visit Permissions
    show_home_visit = models.BooleanField(default=False, verbose_name=_('Manage home visits'))
    add_home_visit = models.BooleanField(default=False, verbose_name=_('Add home visit'))
    delete_home_visit = models.BooleanField(default=False, verbose_name=_('Delete home visit'))
    edit_home_visit = models.BooleanField(default=False, verbose_name=_('Edit home visit'))

    # Custom Medical Tests Permissions
    show_customize_medical_tests = models.BooleanField(default=False, verbose_name=_('Manage custom medical tests'))
    add_customize_medical_tests = models.BooleanField(default=False, verbose_name=_('Add custom medical tests'))
    delete_customize_medical_tests = models.BooleanField(default=False, verbose_name=_('Delete custom medical tests'))
    edit_customize_medical_tests = models.BooleanField(default=False, verbose_name=_('Edit custom medical tests'))

    # Medical Tests Permissions
    show_medical_tests = models.BooleanField(default=False, verbose_name=_('Manage medical tests'))
    view_medical_tests = models.BooleanField(default=False, verbose_name=_('View medical tests'))
    add_medical_tests = models.BooleanField(default=False, verbose_name=_('Add medical tests'))
    delete_medical_tests = models.BooleanField(default=False, verbose_name=_('Delete medical tests'))
    edit_medical_tests = models.BooleanField(default=False, verbose_name=_('Edit medical tests'))
    download_medical_tests = models.BooleanField(default=False, verbose_name=_('Download medical tests'))

    # Medical Visit Reports Permissions
    show_visit_medical_report = models.BooleanField(default=False, verbose_name=_('Manage medical visit reports'))
    view_visit_medical_report = models.BooleanField(default=False, verbose_name=_('View medical visit reports'))
    add_visit_medical_report = models.BooleanField(default=False, verbose_name=_('Add medical visit reports'))
    delete_visit_medical_report = models.BooleanField(default=False, verbose_name=_('Delete medical visit reports'))
    edit_visit_medical_report = models.BooleanField(default=False, verbose_name=_('Edit medical visit reports'))
    download_visit_medical_report = models.BooleanField(default=False, verbose_name=_('Download medical visit reports'))

    edit_settings = models.BooleanField(default=False, verbose_name=_('Edit settings'))


