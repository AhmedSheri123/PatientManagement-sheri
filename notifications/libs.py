from django.utils import timezone
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from accounts.libs import get_user_img
import string, random
from messenger.templatetags.messenger_tags import get_count_of_not_readed_msg

def RandomNumCodeGen(N):
    res = ''.join(random.choices(string.digits, k=N))
    return str(res)


def create_notifications(sender_id, receiver_ids=[], msg='', is_not_readed_toast=False, room_id=''):
    sender = User.objects.get(id=sender_id)
    receivers = User.objects.filter(id__in=receiver_ids)

    sender_img_profile = get_user_img(sender)

    
    for receiver in receivers:
        channel_layer = get_channel_layer()
        receiver_room_id = f'notifications_{str(receiver.id)}'
        toastID = RandomNumCodeGen(6)
        data = {
                'type': 'showToast',
                'method':'showToast',
                'toastID':toastID,
                'username': sender.username,
                'receiver_id': receiver.id,
                'message': msg,
                'img': sender_img_profile[0],
            }
        if is_not_readed_toast:
                data['count_of_not_readed_msg'] = get_count_of_not_readed_msg(receiver.id)
                data['room_id'] = room_id


        async_to_sync(channel_layer.group_send)(
            receiver_room_id,
            data
        )

    return toastID