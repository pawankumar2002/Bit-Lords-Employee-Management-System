from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Employee(models.Model):
    emp= models.OneToOneField(settings.AUTH_USER_MODEL, null=True,on_delete=models.CASCADE)
    img=models.ImageField(upload_to='profilepic',null=True, blank=True,default='profilepic/profile.jpg')
    address=models.TextField(null=True, blank=True)
    phone=models.CharField(max_length=12,null=True, blank=True)
    perDaySalary=models.CharField(max_length=10,default=0)
    bonus=models.CharField(max_length=10,default=0)
    post=models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return str(self.emp)

class Attendance(models.Model):
    emp= models.ForeignKey(settings.AUTH_USER_MODEL, null=True,on_delete=models.CASCADE)
    day=models.IntegerField(null=True,blank=True)
    month=models.CharField(max_length=5,default=0)
    year=models.IntegerField(null=True,blank=True)
    status=models.CharField(max_length=5,default=0)
    task=models.TextField(null=True,blank=True,default="no task for today")
    
    def __str__(self):
        return str(self.day)+'/'+str(self.month)+'/'+str(self.year)+' '+str(self.emp)

class Notice(models.Model):
    title=models.CharField(max_length=30)
    content=models.TextField(null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)



def employee_registration_config(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(emp=instance)
post_save.connect(employee_registration_config, sender=User)
