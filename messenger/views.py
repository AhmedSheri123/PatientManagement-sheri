from django.shortcuts import render, redirect
from .models import MessagesModel, MessengerModel, FavoriteUserModel, BlockUserModel
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from accounts.libs import get_user_img
from django.contrib import messages as dj_messages
from django.views.decorators.clickjacking import xframe_options_exempt


# Create your views here.

@xframe_options_exempt
def messageRoom(request, room_id):
    hospital_profile = request.user.userprofile.hospital_profile
    subscription = hospital_profile.subscription.subscription
    if subscription.one_to_one_chat:
        user = request.user

        messenger = MessengerModel.objects.get(room_id=room_id)
        receiver = messenger.messenger_users.exclude(id=user.id).first()

        is_blocked = BlockUserModel.objects.filter(creator=user, user=receiver).exists()
        is_favorite = FavoriteUserModel.objects.filter(creator=user, user=receiver).exists()
        messages_list = []
        last_date = None
        msg_date = []
        messages = MessagesModel.objects.filter(messenger__room_id=room_id)
        for msg in messages:
            if last_date == None:
                
                last_date=msg.creation_date.date()
            elif msg.creation_date.date() != last_date:
                
                messages_list.append([last_date, msg_date])
                last_date=msg.creation_date.date()
                msg_date = []
                
            msg_date.append(msg)
        messages_list.append([last_date, msg_date])

        profile_image = get_user_img(receiver)
        return render(request, 'messenger/viewMessage.html', {'is_blocked':is_blocked, 'is_favorite':is_favorite, 'messages_list':messages_list, 'room_id':room_id, 'receiver':receiver, 'profile_image':profile_image})
    else:
        dj_messages.error(request, 'هذه الاجراء ليس ضمن مميزات الاشتراك الخاص بك يرجى ترقية الاشتراك حتى تتمكن من استخدام هذه الميزة')
        return redirect('ManageAdminPermission')

def get_messenger_model(sender, receiver):
    messengers = MessengerModel.objects.filter(messenger_users=sender).filter(messenger_users=receiver)
    return messengers

def createMessager(request, receiver_id):
    sender = request.user
    receiver = User.objects.get(id=receiver_id)
    
    messengers = get_messenger_model(sender, receiver)

    if sender != receiver:
        room_id = None
        if not messengers.exists():    
            messenger = MessengerModel.objects.create()
            messenger.messenger_users.set([sender, receiver])
            messenger.save()
            room_id = messenger.room_id
        else:
            room_id = messengers.first().room_id
        return redirect('messageRoom', room_id)
    else:
        return redirect('index')


def AddFavorite(request, receiver_id):
    creator = request.user
    receiver = User.objects.get(id=receiver_id)

    if not FavoriteUserModel.objects.filter(creator=creator, user=receiver).exists():
        fav = FavoriteUserModel.objects.create(creator=creator, user=receiver)
        fav.save()

    room = get_messenger_model(sender=creator, receiver=receiver).first()

    return redirect('messageRoom', room.room_id)



def AddDeleteFavorite(request, receiver_id):
    creator = request.user
    receiver = User.objects.get(id=receiver_id)

    if FavoriteUserModel.objects.filter(creator=creator, user=receiver).exists():
        fav = FavoriteUserModel.objects.filter(creator=creator, user=receiver)
        for f in fav:
            f.delete()
            return JsonResponse({'status':False})
    else:
        fav = FavoriteUserModel.objects.create(creator=creator, user=receiver)
        fav.save()
        return JsonResponse({'status':True})


def DeleteFavorite(request, fav_id):
    sender = request.user
    if request.GET.get('redir'):
        receiver = User.objects.get(id=fav_id)
        room = get_messenger_model(sender=sender, receiver=receiver).first()
        favs = FavoriteUserModel.objects.filter(creator=sender, user=receiver)
        if favs.exists():
            favs.first().delete()
        return redirect('messageRoom', room.room_id)
    else:
        if FavoriteUserModel.objects.filter(id=fav_id).exists():
            fav = FavoriteUserModel.objects.get(id=fav_id)
            receiver = fav.user

            return JsonResponse({'status':True})
        return JsonResponse({'status':False})


def BlockUserMessenger(request, receiver_id):
    creator = request.user
    receiver = User.objects.get(id=receiver_id)
    if not BlockUserModel.objects.filter(creator=creator, user=receiver).exists():
        fav = BlockUserModel.objects.create(creator=creator, user=receiver)
        fav.save()

    room = get_messenger_model(sender=creator, receiver=receiver).first()

    return redirect('messageRoom', room.room_id)

def DeleteBlockUser(request, block_id):
    sender = request.user
    if request.GET.get('redir'):
        receiver = User.objects.get(id=block_id)
        room = get_messenger_model(sender=sender, receiver=receiver).first()
        favs = BlockUserModel.objects.filter(creator=sender, user=receiver)
        if favs.exists():
            favs.first().delete()
        return redirect('messageRoom', room.room_id)
    else:
        if BlockUserModel.objects.filter(id=block_id).exists():
            fav = BlockUserModel.objects.get(id=block_id)
            fav.delete()

            return JsonResponse({'status':True})
        return JsonResponse({'status':False})
    

@xframe_options_exempt
def viewMessages(request):
    user = request.user
    hospital_profile = user.userprofile.hospital_profile
    users = User.objects.filter(Q(userprofile__hospital_profile=hospital_profile, userprofile__profile_type='0') | Q(userprofile__hospital_profile=hospital_profile, userprofile__profile_type='2')).exclude(id=user.id)
    return render(request, 'messenger/viewMessages.html', {'users':users})
UserProfile