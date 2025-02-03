from django.db import models
from django.contrib.auth.models import User
import string
import random
from accounts.libs import when_published
# Create your models here.


def RandomRoomIDGen():
    N = 25
    res = ''.join(random.choices(string.digits, k=N))
    return 'i' + str(res)


class MessengerModel(models.Model):
    messenger_users = models.ManyToManyField(User)

    room_id = models.CharField(max_length=255, default=RandomRoomIDGen)

    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")

class MessagesModel(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    msg = models.TextField()

    messenger = models.ForeignKey(MessengerModel, on_delete=models.CASCADE)

    is_readed = models.BooleanField(default=False)
    is_receiver_subscription_passed = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="تاريخ الانشاء")



    def whenpublished(self):
        return when_published(self.creation_date)
    


class BlockUserModel(models.Model):
    creator = models.ForeignKey(User, related_name="block_creator", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="block_user", on_delete=models.CASCADE)

    creation_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="تاريخ الانشاء")

class FavoriteUserModel(models.Model):
    creator = models.ForeignKey(User, related_name="favorite_creator", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="favorite_user", on_delete=models.CASCADE)

    creation_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="تاريخ الانشاء")