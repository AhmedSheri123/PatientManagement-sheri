from django.shortcuts import render
from messenger.views import get_user_img
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from accounts.models import NotificationsModel
from django.utils import timezone

# Create your views here.

