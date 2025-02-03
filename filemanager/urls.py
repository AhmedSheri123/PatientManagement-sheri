from django.urls import path
from . import views


urlpatterns = [
    path('<str:secret>', views.FileManager, name='FileManager'),
    path('CreateFolder/<str:secret>', views.CreateFolder, name='CreateFolder'),
    path('Rename/<str:secret>', views.Rename, name='Rename'),
    path('Remove/<str:secret>', views.Remove, name='Remove'),
    path('UploadFiles/<str:secret>', views.UploadFiles, name='UploadFiles'),
]
