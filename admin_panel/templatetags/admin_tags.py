from django import template
# from accounts.models import CompanyCreateJobModel, EmployeeJobRequest
from django.contrib.auth.models import User
from accounts.models import UserSubscriptionModel, HospitalsModel

register = template.Library()

@register.simple_tag
def get_hospital_sub(sub_id):
    sub = UserSubscriptionModel.objects.get(id=sub_id)
    hospital = HospitalsModel.objects.filter(subscription=sub)
    if hospital:
        return hospital.first()
    return ''
