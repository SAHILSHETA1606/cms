from importlib import import_module
from django.shortcuts import render
from .models import Medicine
from .resources import MedicineResource
from django.contrib import messages
from tablib import Dataset

# Create your views here.
def Upload_Excel(request):
    if request.method=='POST':
        med_resource=MedicineResource()
        dataset=Dataset()
        new_med=request.FILES['myfile']

        if not new_med.name.endswith('xlsx'):
            messages.info(request,'wrong format valid xlsx')
            return render(request,'upload_medicine.html')

        imported_data=dataset.load(new_med.read(),format='xlsx')
        for data in imported_data:
            value=Medicine(data[0],data[1],data[2],data[3])
            value.save()
    return render(request,'upload_medicine.html')

def view_medicine(request):
    meds=Medicine.objects.all()
    print(meds)
    return render(request,'viewmeds.html',{'meds':meds})