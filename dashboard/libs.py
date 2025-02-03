from bs4 import BeautifulSoup
from django.forms.models import model_to_dict
import io, json
import pandas as pd
from accounts.models import UserProfile, AdminPermissionModel
from django.contrib.auth.models import User
from .models import UploadImageModel

# Create your tests here.



def has_permission(user_id, action, resource):
    user = User.objects.get(id=user_id)

    # إذا كان المستخدم هو superuser، يعاد True دائمًا
    if user.is_superuser:
        return True

    # جلب أذونات المستخدم
    try:
        userprofile = UserProfile.objects.get(id=user.userprofile.id)
        if userprofile.profile_type == '0':
            return True
        permission = AdminPermissionModel.objects.get(id=userprofile.permissions.id)
        if not permission.is_enabled:return False
    except AdminPermissionModel.DoesNotExist:
        return False

    # قائمة الأذونات المتاحة في النموذج
    permissions_mapping = {
        'admin': {
            'show': permission.show_admin,
            'add': permission.add_admin,
            'edit': permission.edit_admin,
            'delete': permission.delete_admin,
        },
        'patient': {
            'show': permission.show_patient,
            'add': permission.add_patient,
            'edit': permission.edit_patient,
            'delete': permission.delete_patient,
        },
        'normal_visit': {
            'show': permission.show_normal_visit,
            'add': permission.add_normal_visit,
            'edit': permission.edit_normal_visit,
            'delete': permission.delete_normal_visit,
        },
        'home_visit': {
            'show': permission.show_home_visit,
            'add': permission.add_home_visit,
            'edit': permission.edit_home_visit,
            'delete': permission.delete_home_visit,
        },
        'customize_medical_tests': {
            'show': permission.show_customize_medical_tests,
            'add': permission.add_customize_medical_tests,
            'edit': permission.edit_customize_medical_tests,
            'delete': permission.delete_customize_medical_tests,
        },
        'medical_tests': {
            'show': permission.show_medical_tests,
            'view': permission.view_medical_tests,
            'add': permission.add_medical_tests,
            'edit': permission.edit_medical_tests,
            'delete': permission.delete_medical_tests,
            'download': permission.download_medical_tests,
        },
        'visit_medical_report': {
            'show': permission.show_visit_medical_report,
            'view': permission.view_visit_medical_report,
            'add': permission.add_visit_medical_report,
            'edit': permission.edit_visit_medical_report,
            'delete': permission.delete_visit_medical_report,
            'download': permission.download_visit_medical_report,
        },
        'settings': {
            'edit': permission.edit_settings,
        },
        'index': {
            'show': permission.show_index,
        }
    }

    # التحقق من الإذن بناءً على المورد والإجراء
    if resource in permissions_mapping:
        resource_permissions = permissions_mapping[resource]
        return resource_permissions.get(action, False)

    # إذا لم يكن المورد أو الإجراء معروفين، يعاد False
    return False

def get_general_settings(file_path):

    file = open(file_path, 'r')
    settings = {}
    img_obj = None
    data = file.read()
    if data:
        settings = json.loads(data)
        if settings.get('img_id'):
            try:
                img_obj = UploadImageModel.objects.get(id=settings.get('img_id'))
            except:img_obj=''
    file.close()
    return settings, img_obj

def medical_tests_html_to_dict(data):
    html = data.get('form-box-content')
    soup = BeautifulSoup(html.encode('utf-8'), 'html.parser')
    out = []
    el_boxs = soup.find_all('div', class_='ele-box')
    counter = 0

    for el_box in el_boxs:
        counter +=1

        if el_box['data-type'] == 'title':
            name = el_box.find('input', class_='title')['name']
            value = data[name]
            out.append({
                'id':str(counter),
                'data_type':el_box['data-type'],
                'title': value,
            })

        elif el_box['data-type'] == 'el-text':
            el_title_name = el_box.find('input', class_='el-title')['name']
            el_unit_name = el_box.find('input', class_='el-unit')['name']
            el_maximum_name = el_box.find('input', class_='el-maximum')['name']
            el_minimum_name = el_box.find('input', class_='el-minimum')['name']

            el_title_value = data[el_title_name]
            el_unit_value = data[el_unit_name]
            el_maximum_value = data[el_maximum_name]
            el_minimum_value = data[el_minimum_name]

            out.append({
                'id':str(counter),
                'data_type':el_box['data-type'],
                'el_title': el_title_value,
                'el_unit': el_unit_value,
                'el_maximum': el_maximum_value,
                'el_minimum': el_minimum_value,
            })
    return out

def medical_test_scraper(post_data, data):
    
    for el in data:
        if el.get('data_type') == 'el-text':
            id = el.get('id')
            data[data.index(el)]['el_result'] = post_data.get(f'el_result{id}')

    return data


# def ModelToDoc(models=None, fields=None):
#     # Example:
#     # byte = ModelToDoc(models=User.objects.all())
#     # f = open('aaaa.xlsx', 'wb')
#     # f.write(byte)
#     # f.close()

#     #get model fields
#     out_fields = {}
#     fields_obj = models.model._meta.fields
#     for f in fields_obj:
#         if not fields:
#             if f.name == 'user':
#                 print(f.model._meta.fields)
#             out_fields[fields_obj.index(f)] = []
#         else:
#             if f.name in fields:
#                 out_fields[fields_obj.index(f)] = []
#     #get model values
#     for model in models:
#         data_dict = model_to_dict(model, fields=fields)

#         for field_name, value in data_dict.items():
#             for field_obj in fields_obj:
#                 if field_obj.name == field_name:
#                     #str, NoneType, date, datetime, bool
#                     if type(value).__name__ == 'datetime':
#                         value = str(value)
#                     out_fields[fields_obj.index(field_obj)].append(value)

#     for f in fields_obj:
#         field_name = f.name
#         field_verbose = models.model._meta.get_field(field_name).verbose_name

#         if not fields:
#             out_fields[field_verbose] = out_fields[fields_obj.index(f)]
#             del out_fields[fields_obj.index(f)]
#         else:
#             if f.name in fields:
#                 out_fields[field_verbose] = out_fields[fields_obj.index(f)]
#                 del out_fields[fields_obj.index(f)]



#     marks_data = pd.DataFrame(out_fields)
#     buffer = io.BytesIO()
#     marks_data.to_excel(buffer)
#     buffer.seek(0)
#     return buffer


from django.db.models.fields.related import ForeignKey, OneToOneField

def get_all_model_fields(models, postion=''):
    out_fields = {}
    fields_obj = models.model._meta.fields
    # print(models)
    for f in fields_obj:
        field_name = postion + f.name
        if f.__class__ is ForeignKey or f.__class__ is OneToOneField:
            field_name = f.name + '__'
            out_fields.update(get_all_model_fields(f.remote_field, postion=field_name))
            continue
        out_fields[field_name] = []
    return out_fields


def get_all_model_fields_values(models, fields):
    for field in fields:
        try:
            querys_set = models.values(field)
        except:
            continue
        for query_set in querys_set:
            value = query_set[field]
            if type(value).__name__ == 'datetime':value = str(value)

            fields[field].append(value)
    return fields

def get_data_export(data={}, export_format=''):
    buffer = io.BytesIO()
    out_buffer = b''

    marks_data = pd.DataFrame(data)
    if export_format == 'xlsx':
        marks_data.to_excel(buffer)
        buffer.seek(0)
        out_buffer = buffer

    elif export_format == 'html':
        buffer_str = marks_data.to_html()
        out_buffer = buffer_str

    elif export_format == 'csv':
        marks_data.to_csv(buffer)
        buffer.seek(0)
        out_buffer = buffer

    elif export_format == 'json':
        marks_data.to_json(buffer)
        buffer.seek(0)
        out_buffer = buffer

    return out_buffer

def ModelToDoc(models=None, fields=None, rename_fields=[], export_format='xlsx'):
    result = {}

    all_fields = get_all_model_fields(models, postion='')
    fields_with_values = get_all_model_fields_values(models, all_fields)
    if fields:
        for field in fields:
            result[field] = fields_with_values[field]
    else:
        result = fields_with_values

    if rename_fields:
        out = {}
        for field, values in result.items():
            if field in rename_fields:
                out[rename_fields[field]] = values
            else:
                out[field] = values

        result = out


    buffer = get_data_export(result, export_format)
    return buffer