from django.db import models

# Create your models here.
class Medicine(models.Model):
    medicine_name=models.CharField(max_length=30)
    medicine_power=models.CharField(max_length=30)
    medicine_price=models.IntegerField(blank=True,null=False)

    def __str__(self):
        return self.medicine_name +''+ self.medicine_power