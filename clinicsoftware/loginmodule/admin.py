from django.contrib import admin

# Register your models here.
from .models import patient_detail
from .models import patient_health_detail
from .models import Patient_group
from .models import Account
admin.site.register(patient_detail)
admin.site.register(patient_health_detail)
admin.site.register(Patient_group)
admin.site.register(Account)
