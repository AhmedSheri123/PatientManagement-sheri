from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
import os, datetime, time
import shutil
from django.http import JsonResponse
from dashboard.subscription_rules import get_hospital_disk_info, hosptial_storage_size_mb_rule
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
BASE_DIR = settings.BASE_DIR

img_formats_list = ['.jpg', '.png', '.webp', '.gif', '.tif', '.bmp', '.eps']

def path_cleaner(path):
    path = path.replace('//', '/')
    path = path.replace('\\', '/')
    path = path.replace('\\\\', '/')
    return path

def get_path(request, secret, path):
    hospital_id, user_id = secret.split('-', 1)
    user = request.user
    user_path = f'media/manager/{hospital_id}/{user_id}'
    if user_path in path:
        path = path.split(user_path, 1)[1]
    return path

def get_back_path(current_path):
    if current_path !='/':
        if current_path.endswith('/'):
            current_path = path_cleaner((current_path.rsplit('/', 2)[0]) + '/')
        else:
            current_path = path_cleaner((current_path.rsplit('/', 1)[0]) + '/')
    return current_path


def get_current_path(request, secret):
    current_path = None
    current_path = request.GET.get('path')
    if not current_path: current_path = '/'

    current_path = get_path(request, secret, current_path)
    current_path = path_cleaner(current_path)
    return current_path

def get_full_path(request, secret):
    user = request.user
    hospital_id, user_id = secret.split('-', 1)
    user_path = f'media/manager/{hospital_id}/{user_id}'
    current_path = get_current_path(request, secret)
    full_path = user_path + current_path
    full_path = path_cleaner(full_path)
    return full_path

def get_file_path(full_path, file):
    file_path = full_path + file
    return file_path

def get_base_path(path):
    base_path = str(BASE_DIR / str(path))
    if os.path.isdir(base_path):
        base_path = base_path+'/'
    base_path = path_cleaner(base_path)
    return base_path

def get_folder_contents(full_path):
    base_path = get_base_path(full_path)
    contents = os.listdir(base_path)
    obj = []
    for content in contents:
        content_path = base_path + content
        url = path_cleaner('/'+full_path + content)

        name, format = os.path.splitext(content_path)
        name = name.rsplit('/', 1)[1]
        full_name = name + format

        ti_m = os.path.getmtime(content_path)
        t_obj = datetime.datetime.fromtimestamp(ti_m)

        out = {'type':''}
        
        out['name']=name
        out['m_datetime']=t_obj
        out['full_name']=full_name
        
        if os.path.isfile(content_path):
            out['url']=url
            out['type'] = 'file';out['format']=format
            if format in img_formats_list:
                out['type'] = 'img'

        elif os.path.isdir(content_path):
            out['type'] = 'folder'
            out['url']=path_cleaner(url+'/')
        obj.append(out)
    return obj

def sys_create_folder(full_path):
    os.mkdir(full_path)

def sys_rename(old_path, new_path):
    os.rename(old_path, new_path)

def sys_remove_items(path_list, request, secret):
    for path in path_list:
        path = path_cleaner(get_base_path(get_full_path(request, secret) + path))
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)


def FileManager(request, secret):
    hospital_profile = request.user.userprofile.hospital_profile
    hospital_used_storage = get_hospital_disk_info(request.user).get('used', 0)
    hospital_used_storage = int(hospital_used_storage/(1024*1024))
    hospital_max_storage = hospital_profile.subscription.subscription.hosptial_storage_size_mb
    print()
    percentage_used_storage = int((hospital_used_storage/ hospital_max_storage) * 100)

    current_path = get_current_path(request, secret)
    splited_current_path = current_path.split('/')
    back_path = get_back_path(current_path)
    full_path = get_full_path(request, secret)
    
    contents = get_folder_contents(full_path)
    return render(request, 'file-manager/manager.html', {'contents':contents, 'back_path':back_path, 'current_path':current_path, 'splited_current_path':splited_current_path, 'secret':secret, 'hospital_used_storage':hospital_used_storage, 'hospital_max_storage':hospital_max_storage, 'percentage_used_storage':percentage_used_storage})


def CreateFolder(request, secret):
    current_path = get_current_path(request, secret)
    folder_name = request.GET.get('folder_name')
    if folder_name:
        full_path = path_cleaner(get_base_path(get_full_path(request, secret) + folder_name))
        sys_create_folder(full_path)
        new_path = path_cleaner(current_path+folder_name)
    return redirect(reverse('FileManager', kwargs={'secret':secret})+f'?path={new_path}/')

def Rename(request, secret):
    current_path = get_current_path(request, secret)
    old_name = request.GET.get('old_name')
    new_name = request.GET.get('new_name')

    if new_name and old_name:
        old_name_full_path = path_cleaner(get_base_path(get_full_path(request, secret) + old_name))
        new_name_full_path = path_cleaner(get_base_path(get_full_path(request, secret) + new_name))
        sys_rename(old_name_full_path, new_name_full_path)
    return redirect(reverse('FileManager', kwargs={'secret':secret})+f'?path={current_path}')

def Remove(request, secret):
    current_path = get_current_path(request, secret)
    if request.method == 'POST':
        items = request.POST.getlist('items')
        if items:
            sys_remove_items(items, request, secret)
    return redirect(reverse('FileManager', kwargs={'secret':secret})+f'?path={current_path}')


def sysUploadFiles(request, secret, path):
    path = path_cleaner(get_base_path(get_full_path(request, secret) + path))
    
    files = request.FILES.getlist('file', '')
    for file in files:
        if file:
            full_path = path+file.name
            writer = open(full_path, 'wb')
            writer.write(file.read())
            writer.close()

@csrf_exempt
def UploadFiles(request, secret):
    if request.method == 'POST':
        files = request.FILES.getlist('file', [])
        files_size = 0
        for file in files:
            files_size += file.size
        if hosptial_storage_size_mb_rule(request.user, files_size):
            path = request.POST.get('path')
            sysUploadFiles(request, secret, path)
            return JsonResponse({"success":True})
    
    return JsonResponse({"success":False})