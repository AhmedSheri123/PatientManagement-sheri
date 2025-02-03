from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.Login, name='Login'),
    path('Logout', views.Logout, name='Logout'),
    path('GetSubscriptionsPlanInfoAPI', views.GetSubscriptionsPlanInfoAPI, name='GetSubscriptionsPlanInfoAPI'),
    path('AddHospitalsByAPI', views.AddHospitalsByAPI, name='AddHospitalsByAPI'),
    path('RenewSubscription/<int:user_id>', views.RenewSubscription, name='RenewSubscription'),
    path('GetPatientManagementInfo/<int:id>', views.GetPatientManagementInfo, name='GetPatientManagementInfo'),
    path('DeletePatientManagementAPI/<int:id>', views.DeletePatientManagementAPI, name='DeletePatientManagementAPI'),
    path('ResetPasswordAPI/<int:id>', views.ResetPasswordAPI, name='ResetPasswordAPI'),
    
]