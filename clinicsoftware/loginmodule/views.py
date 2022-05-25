
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User,auth
from django.core.mail import send_mail
import math, random
from django.db.models import Q
from .models import patient_detail
from .models import patient_health_detail
from .models import Patient_group
from .models import Account
from medicine.models import Medicine
import datetime
import json as simplejson
import json
# Create your views here.
def home(request):

    patient = patient_detail.objects.all()
    return render(request,'home.html',{'patient':patient})

def addpatient(request):
    return render(request,'addpatient.html')

def patient_details(request):

    if request.method=="POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        blood_group = request.POST['blood_group']
        age = request.POST['age']
        weight = request.POST['weight']
        contact = request.POST['contact']
        address = request.POST['address']
        rperson = request.POST['rperson']

        user = patient_detail( fname = fname,lname = lname,blood_group = blood_group,age = age, weight =  weight,contact = contact,address = address , rperson = rperson)
        user.save()

        return redirect('/')
    else:
        return render(request,'home.html')

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

def addpatient_health_details(request,i):
    patient_health = patient_detail.objects.get(id=i)
    medi=Medicine.objects.all()
    return render(request,'addpatient_health.html',{'patient':patient_health,'pid':patient_health.id,'medi':medi})

def patient_health_details(request,i):
    if request.method=="POST":
        t1=patient_detail.objects.get(id=i)
        fname=t1.fname
        lname=t1.lname
        symptoms = request.POST['symptoms']
        diagnostic = request.POST['diagnostic']
        prescription = request.POST.getlist('prescription')
        report = request.POST['report']
        fees = request.POST['fees']
        paid = request.POST['paid']
        date = datetime.date.today()
        time=datetime.datetime.now().time()
        #t1=patient_detail.objects.get(patient_id=i)
        #t2=t1.id
        user = patient_health_detail(patient_id=i,fname = fname,lname = lname,symptoms=symptoms,diagnostic=diagnostic,report=report,date=date,time=time,fees=fees,paid=paid)
        listIWantToStore = prescription
        user.prescription = json.dumps(listIWantToStore)
        user.save()
        patient = patient_detail.objects.all()
        return render(request,'home.html',{'patient':patient})

def visit_summary(request):
    patient = patient_detail.objects.all()
    return render(request,'visit_summary.html',{'patient':patient})

def particular_person_summary(request,i):
    visit=patient_health_detail.objects.filter(patient_id=i).all()
    #print("-------------------------------------------------")
    #print(visit.patient_visit)
    #print("-------------------------------------------------")
    s={'patient':visit,'id':i}
    return render(request,'particular_patient.html',s)
    
def calclulation(i,j,pid):
    if i == j:
        return 0
    elif i > j:
        c=i-j
        Account.objects.filter(patient_id = pid).update(tleft_from_patient=c,tleft_from_doc=0)
        return c
    elif j > i:
        c=j-i
        Account.objects.filter(patient_id = pid).update(tleft_from_doc=c,tleft_from_patient=0)
        return c
    
def summary(request,i,j):
    s=patient_health_detail.objects.get(id=i)
    #j is patient id i is visit no
    pid=j
    p1=patient_detail.objects.get(id=pid)
    paid=s.paid
    fees=s.fees
    d=patient_health_detail.objects.filter(patient_id=pid)
    Total_FEES=0
    Total_PAID=0
    for g in d:
     Total_FEES=Total_FEES+g.fees
     Total_PAID=Total_PAID+g.paid
    
    try:
     t=Account.objects.get(patient_id=pid)
     if t != None:
      Account.objects.filter(patient_id = pid).update(tfees=Total_FEES,tpaid=Total_PAID)
      t=Account.objects.get(patient_id=pid)
    except:
     
     Account(patient_id=p1,tfees=Total_FEES,tpaid=Total_PAID).save()
     t=Account.objects.get(patient_id=pid)

    if fees == paid:
        calclulation(Total_FEES,Total_PAID,pid)
        summary={'s':s,'t':t}
        return render(request,'summary.html',summary)
    elif paid < fees:
        calclulation(Total_FEES,Total_PAID,pid)
        pleft=fees-paid
        patient_health_detail.objects.filter(id=i).update(left_from_patient=pleft)
        s=patient_health_detail.objects.get(id=i)
        t=Account.objects.get(patient_id=pid)
        summary={'s':s,'t':t}
        return render(request,'summary.html',summary)
    elif paid > fees:
        calclulation(Total_FEES,Total_PAID,pid)
        dleft=paid-fees
        patient_health_detail.objects.filter(id=i).update(left_from_doc=dleft)
        s=patient_health_detail.objects.get(id=i)
        t=Account.objects.get(patient_id=pid)
        summary={'s':s,'t':t}
        return render(request,'summary.html',summary)

def patient_group(request): 
    
    p = patient_detail.objects.all()
    return render(request,'patient_group.html',{'patient':p})

def create_group(request): 
    if request.method=="POST":
        mem = request.POST.getlist('mselect')
        mem_sep = []
        for i in mem:
         mem_sep.append(i.split(":"))
        print("-------------------------------------------------")
        print(mem)
        print(mem_sep)
        print(mem_sep[0][0])
        print("-------------------------------------------------")
        gname = request.POST['gname']
        user=Patient_group(gname=gname)
        listIWantToStore = mem_sep
        user.member = json.dumps(listIWantToStore)
        user.save()
        g = Patient_group.objects.all()
        s={'group':g}
        return redirect('/all_group')
        
    else:
         p = patient_detail.objects.all()
         s={'patient':p}
         return render(request,'patient_group.html',s)
        
def all_group(request): 
    g = Patient_group.objects.all()    
    s={'group':g}
    return render(request,'all_group.html',s)

def particular_group(request,i):
    g=Patient_group.objects.get(id=i)
    jsonDec = json.decoder.JSONDecoder()
    gList = jsonDec.decode(g.member)
    mem_sep = []
    
    for j in gList:
        mem_sep.append({"id":j[0],"name":j[1]})
        
    #print("-------------------------------------------------")
    #print(mem_sep)
    #print(mem_sep[0]["id"])
    #print("-------------------------------------------------")
    Total_Group_paid=0
    Total_Group_fees=0
    Total_Group_from_patient=0
    Total_Group_from_doc=0
    
    dleft_account = []
    pleft_account = []
    print("-------------------------------------------------")
    for i in gList:
        #print(i[0])#pid is patient id
        pid = i[0]
        print(pid)
    #print("-------------------------------------------------")
        o = Account.objects.get(patient_id=pid)
        o1 = patient_detail.objects.get(id=pid)
        print(o.tfees)
        print(o1)
   
        Total_Group_paid=Total_Group_paid+o.tpaid
        Total_Group_fees=Total_Group_fees+o.tfees
        Total_Group_from_patient=Total_Group_from_patient+o.tleft_from_patient
        Total_Group_from_doc=Total_Group_from_doc+o.tleft_from_doc

        if o.tleft_from_patient != 0:
            pleft_account.append({'fname':o1.fname,'lname':o1.lname,'left':o.tleft_from_patient})
        elif o.tleft_from_doc != 0:
            dleft_account.append({'fname':o1.fname,'lname':o1.lname,'left':o.tleft_from_doc}) 
    
    print("-------------------------------------------------")
        
    p = patient_detail.objects.all()
    s={'list':mem_sep,'patient':p,'tpaid':Total_Group_fees,'tfees':Total_Group_paid,'tfrom_patient':Total_Group_from_patient,'tfrom_doc':Total_Group_from_doc,'list_pleft':pleft_account,'list_dleft':dleft_account}
    return render(request,'particular_group.html',s)
