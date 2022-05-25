from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Medicine
# Register your models here.
@admin.register(Medicine)
class Medicineadmin(ImportExportModelAdmin):
    list_display=('medicine_name','medicine_power','medicine_price')