from django.urls import path
from . import views

urlpatterns = [
    path('', views.PanelHome, name='PanelHome'),
    path('ManagePatients', views.ManagePatients, name='ManagePatients'),
    path('AddPatients', views.AddPatients, name='AddPatients'),
    path('EditPatients/<int:id>', views.EditPatients, name='EditPatients'),
    path('DeletePatient/<int:id>', views.DeletePatient, name='DeletePatient'),


    #Vists
    path('ManagePatientVisits', views.ManagePatientVisits, name='ManagePatientVisits'),
    path('AddPatientVisit', views.AddPatientVisit, name='AddPatientVisit'),
    path('EditPatientVisit/<int:id>', views.EditPatientVisit, name='EditPatientVisit'),
    path('DeletePatientVisit/<int:id>', views.DeletePatientVisit, name='DeletePatientVisit'),
    
    #Home Visit
    path('ManagePatientHomeVisits', views.ManagePatientHomeVisits, name='ManagePatientHomeVisits'),
    path('AddPatientHomeVisit', views.AddPatientHomeVisit, name='AddPatientHomeVisit'),
    path('EditPatientHomeVisit/<int:id>', views.EditPatientHomeVisit, name='EditPatientHomeVisit'),
    path('DeletePatientHomeVisit/<int:id>', views.DeletePatientHomeVisit, name='DeletePatientHomeVisit'),


    #Reports
    path('AddMedicalReport/<int:id>', views.AddMedicalReport, name='AddMedicalReport'),
    path('EditMedicalReport/<int:id>', views.EditMedicalReport, name='EditMedicalReport'),
    path('ViewMedicalReport/<int:id>', views.ViewMedicalReport, name='ViewMedicalReport'),
    path('ManageVisitMedicalReport/<int:id>', views.ManageVisitMedicalReport, name='ManageVisitMedicalReport'),
    path('DeleteMedicalReport/<int:id>', views.DeleteMedicalReport, name='DeleteMedicalReport'),


    path('MedicalReportToPDF/<int:id>', views.MedicalReportToPDF, name='MedicalReportToPDF'),

    #CustomizeMedicalTests
    path('ManageCustomizeMedicalTests', views.ManageCustomizeMedicalTests, name='ManageCustomizeMedicalTests'),
    path('AddCustomizeMedicalTests', views.AddCustomizeMedicalTests, name='AddCustomizeMedicalTests'),
    path('EditCustomizeMedicalTests/<int:id>', views.EditCustomizeMedicalTests, name='EditCustomizeMedicalTests'),
    path('DeleteCustomizeMedicalTests/<int:id>', views.DeleteCustomizeMedicalTests, name='DeleteCustomizeMedicalTests'),
    
    #MedicalTests
    path('MedicalTestsManagePatients', views.MedicalTestsManagePatients, name='MedicalTestsManagePatients'),
    path('ManageMedicalTests/<int:patient_id>', views.ManageMedicalTests, name='ManageMedicalTests'),
    path('AddMedicalTests/<int:patient_id>', views.AddMedicalTests, name='AddMedicalTests'),
    path('EditMedicalTests/<int:id>', views.EditMedicalTests, name='EditMedicalTests'),
    path('ViewMedicalTests/<int:id>', views.ViewMedicalTests, name='ViewMedicalTests'),
    path('DeleteMedicalTests/<int:id>', views.DeleteMedicalTests, name='DeleteMedicalTests'),

    path('MedicalTestsReportToPDF/<int:id>', views.MedicalTestsReportToPDF, name='MedicalTestsReportToPDF'),

    #Settings
    path('GeneralSettings', views.GeneralSettings, name='GeneralSettings'),

    #AdminPermission
    path('ManageAdminPermission', views.ManageAdminPermission, name='ManageAdminPermission'),
    path('AddAdminPermission', views.AddAdminPermission, name='AddAdminPermission'),
    path('EditAdminPermission/<int:id>', views.EditAdminPermission, name='EditAdminPermission'),
    path('DeleteAdminPermission/<int:id>', views.DeleteAdminPermission, name='DeleteAdminPermission'),


    path('PayPatientNormalVisit/<int:id>', views.PayPatientNormalVisit, name='PayPatientNormalVisit'),
    path('PayPatientHomeVisit/<int:id>', views.PayPatientHomeVisit, name='PayPatientHomeVisit'),
    
    
    
    path('PatientsSelectedUsers', views.PatientsSelectedUsers, name='PatientsSelectedUsers'),
]