from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
     path('',views.home, name='home'),
     path('addpatient',views.addpatient, name='addpatient'),
     path('patient_details',views.patient_details, name='patient_details'),
     path('addpatient_health_details/<int:i>',views.addpatient_health_details, name='addpatient_health_details'),
     path('patient_health_details/<int:i>',views.patient_health_details, name='patient_health_details'),
     path('visit_summary',views.visit_summary, name='visit_summary'),
     path('particular_person_summary/<int:i>/',views.particular_person_summary, name='particular_person_summary'),
     path('summary/<int:i>/<int:j>',views.summary, name='summary'),
     path('patient_group',views.patient_group, name='patient_group'),
     path('all_group',views.all_group, name='all_group'),
     path('create_group',views.create_group, name='create_group'),
     path('particular_group/<int:i>',views.particular_group, name='particular_group'),
     path('addpatient_health_details/<str:fname>/<str:lname>',views.addpatient_health_details, name='addpatient_health_details'),


]