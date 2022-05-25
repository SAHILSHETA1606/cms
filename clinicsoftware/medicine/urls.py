from . import views
from django.urls import path,include
urlpatterns = [
    path('',views.Upload_Excel,name='uploadfile' ),
    path('viewMeds/',views.view_medicine ,name='view'),
]