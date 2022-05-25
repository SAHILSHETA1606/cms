from import_export import resources
from .models import Medicine
class MedicineResource(resources.ModelResource):
    class meta:
        model=Medicine