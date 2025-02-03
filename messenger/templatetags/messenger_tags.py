from django import template
from django.template.defaultfilters import stringfilter
from messenger.models import MessagesModel, MessengerModel, BlockUserModel, FavoriteUserModel
from accounts.libs import get_user_img
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.conf import settings

register = template.Library()

@register.simple_tag
@stringfilter
def get_messengers(user_id):
    messengers = MessengerModel.objects.filter(messenger_users__id__in=[user_id])
    for messenger in messengers:
        msgs = MessagesModel.objects.filter(messenger=messenger)
        if not msgs.exists():
            messengers = messengers.exclude(id=messenger.id)
    return messengers

@register.simple_tag
@stringfilter
def get_last_msg(messenger_id, receiver):
    messenger = MessengerModel.objects.get(id = messenger_id)
    messages = MessagesModel.objects.filter(messenger=messenger)
    messages = messages.exclude(sender=receiver)
    if messages.exists():
        msg = messages.order_by('-id').first()
        if not msg.is_receiver_subscription_passed:
            msg.msg = 'نفذ عدد استقبال الرسائل يرجى ترقية او تجديد العضوية لاظهار الرسالة'

        return msg
    return ''

@register.simple_tag
@stringfilter
def get_last_msg_by_sender_receiver(sender, receiver):
    messenger = MessengerModel.objects.filter(messenger_users__id__in=[sender]).filter(messenger_users__id__in=[receiver]).first()
    messages = MessagesModel.objects.filter(messenger=messenger)
    messages = messages.exclude(sender=sender)
    if messages.exists():
        msg = messages.order_by('-id').first()
        if not msg.is_receiver_subscription_passed:
            msg.msg = 'نفذ عدد استقبال الرسائل يرجى ترقية او تجديد العضوية لاظهار الرسالة'

        return msg
    return ''

@register.simple_tag
@stringfilter
def get_not_readed_msg_by_sender_receiver(sender, receiver):
    messenger = MessengerModel.objects.filter(messenger_users__id__in=[sender]).filter(messenger_users__id__in=[receiver]).first()
    messages = MessagesModel.objects.filter(messenger=messenger, is_readed=False)
    messages = messages.exclude(sender=sender)
    return messages

@register.simple_tag
@stringfilter
def get_user_profile_img(user_id):
    if user_id:
        user = User.objects.get(id=user_id)
        img = get_user_img(user)

        return img

@register.simple_tag
@stringfilter
def get_receiver_user(sender_id, room_id):
    messenger = MessengerModel.objects.get(room_id=room_id)
    receiver = messenger.messenger_users.exclude(id=sender_id).first()

    return receiver

@register.simple_tag
@stringfilter
def get_favorite_users(user):
    fav = FavoriteUserModel.objects.filter(creator=user)
    return fav

@register.simple_tag
@stringfilter
def get_blocked_users(user):
    blockers = BlockUserModel.objects.filter(creator=user)
    return blockers

@register.simple_tag
@stringfilter
def get_count_of_not_readed_msg(user_id):
    count = 0
    messengers = MessengerModel.objects.filter(messenger_users__id__in=[user_id])
    for messenger in messengers:
        messages = MessagesModel.objects.filter(messenger=messenger, is_readed=False).exclude(sender__id=user_id)
        count += messages.count()
    if count >= 99:
        count  = str(count)+'+'
    if count <= 0:
        count = ''
    return count

@register.simple_tag
@stringfilter
def get_user_full_name(user_id):
    full_name = ''
    if user_id:
        user = User.objects.get(id=user_id)
        alias_obj = user.userprofile.get_account_alias_name_display()
        alias = alias_obj if alias_obj else ''
        full_name =  alias +' - '+ user.first_name +' '+ user.last_name

    return full_name
    
@register.simple_tag
@stringfilter
def get_ws_type(ss):
    a = settings.WS_TYPE
    return a