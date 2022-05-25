from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
# Create your models here.

class patient_detail(models.Model):
    patient_id=models.AutoField
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    blood_group = models.CharField(max_length=5)
    age = models.IntegerField()
    weight = models.IntegerField()
    contact = models.IntegerField()
    address  = models.CharField(max_length=50)
    rperson = models.CharField(max_length=20)
    
    def __str__(self):
         return self.fname +' '+ self.lname

class patient_health_detail(models.Model):
    patient_visit=models.AutoField
    patient_id=models.IntegerField(default=0)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    symptoms = models.CharField(max_length=30)
    diagnostic = models.CharField(max_length=30)
    prescription= models.TextField(max_length=30)
    report = models.CharField(max_length=30)
    date = models.DateField(default=datetime.now, blank=True)
    time=models.TimeField(default=datetime.now, blank=True)
    fees = models.IntegerField(default=0)
    paid = models.IntegerField(default=0)
    left_from_patient=models.IntegerField(default=0)
    left_from_doc=models.IntegerField(default=0)
    
    def __str__(self):
         return self.fname +' '+ self.lname

class Account(models.Model):
    patient_id = models.OneToOneField(patient_detail, on_delete=models.CASCADE,primary_key=True)
    tfees = models.IntegerField(default=0)
    tpaid = models.IntegerField(default=0)
    tleft_from_patient=models.IntegerField(default=0)
    tleft_from_doc=models.IntegerField(default=0)

class Patient_group(models.Model):
    gid = models.AutoField
    gname =  models.CharField(max_length=20)
    member = models.TextField(null=True)
    tfees = models.IntegerField(default=0)
    tpaid = models.IntegerField(default=0)
    tleft_from_patient=models.IntegerField(default=0)
    tleft_from_doc=models.IntegerField(default=0)

    def __str__(self):
         return self.gname
