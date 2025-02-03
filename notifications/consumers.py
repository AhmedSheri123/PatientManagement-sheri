import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.utils import timezone
from channels.layers import get_channel_layer
from messenger.models import MessagesModel
from accounts.libs import get_user_img
from messenger.templatetags.messenger_tags import get_count_of_not_readed_msg


class chatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.msg_model = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'notifications_{self.room_name}'
        user = self.scope["user"]

        # connection has to be accepted
        self.accept()
        
        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )


        userprofile = UserProfile.objects.get(id=user.userprofile.id)
        userprofile.is_active = True
        userprofile.save()
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'method':'msg_read_all',
                'user_id': user.id,
            }
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

        user = self.scope["user"]
        userprofile = UserProfile.objects.get(id=user.userprofile.id)
        userprofile.is_active = False
        userprofile.last_active_datetime = timezone.now()
        userprofile.save()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        method = text_data_json['method']
        user = self.scope["user"]
        

        # send chat message event to the room
        if method == 'showToast':

            receiver_id = text_data_json['receiver_id']
            receiver=User.objects.get(id=receiver_id)
            img = get_user_img(user)
            msg_id = text_data_json['msg_id']

            msg_model = MessagesModel.objects.get(id=msg_id)

            if not msg_model.is_receiver_subscription_passed:
                msg_model.msg = 'نفذ عدد استقبال الرسائل يرجى ترقية او تجديد العضوية لاظهار الرسالة'


            channel_layer = get_channel_layer()
            receiver_room_id = f'notifications_{str(receiver_id)}'

            async_to_sync(channel_layer.group_send)(
                receiver_room_id,
                {
                    'type': 'showToast',
                    'method':method,
                    'toastID':msg_model.id,
                    'username': user.username,
                    'message': msg_model.msg,
                    'img': img[0],
                    'count_of_not_readed_msg':get_count_of_not_readed_msg(receiver_id)

                }
            )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def showToast(self, event):
        self.send(text_data=json.dumps(event))

# code src = https://testdriven.io/blog/django-channels/, https://www.youtube.com/watch?v=cw8-KFVXpTE
