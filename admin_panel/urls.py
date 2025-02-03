from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='admin_panel_index'),

    #Hospitals
    path('ManageHospitals', views.ManageHospitals, name='ManageHospitals'),
    path('AddHospitals', views.AddHospitals, name='AddHospitals'),
    path('EditHospitals/<int:id>', views.EditHospitals, name='EditHospitals'),
    path('DeleteHospitals/<int:id>', views.DeleteHospitals, name='DeleteHospitals'),

    #HospitalAdmins
    path('ManageHospitalAdmins', views.ManageHospitalAdmins, name='ManageHospitalAdmins'),
    path('AddHospitalAdmins', views.AddHospitalAdmins, name='AddHospitalAdmins'),
    path('EditHospitalAdmins/<int:id>', views.EditHospitalAdmins, name='EditHospitalAdmins'),
    path('DeleteHospitalAdmins/<int:id>', views.DeleteHospitalAdmins, name='DeleteHospitalAdmins'),

    #Subscriptions
    path('ManageSubscriptions', views.ManageSubscriptions, name='ManageSubscriptions'),
    path('AddSubscription', views.AddSubscription, name='AddSubscription'),
    path('EditSubscription/<int:id>', views.EditSubscription, name='EditSubscription'),
    path('DeleteSubscription/<int:id>', views.DeleteSubscription, name='DeleteSubscription'),

    #UserSubscriptions
    path('ManageUserSubscriptions', views.ManageUserSubscriptions, name='ManageUserSubscriptions'),
    path('AddUserSubscription', views.AddUserSubscription, name='AddUserSubscription'),
    path('EditUserSubscription/<int:id>', views.EditUserSubscription, name='EditUserSubscription'),
    path('DeleteUserSubscription/<int:id>', views.DeleteUserSubscription, name='DeleteUserSubscription'),
]