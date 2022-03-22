from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class Student(AbstractUser):
  
    # username = models.CharField(max_length=255,blank=True,null=True)
    mobile = models.IntegerField(blank=True,null=True)
    course = models.CharField(max_length=255,blank=True,null=True)
    section = models.CharField(max_length=255,blank=True,null=True)
    # password = models.CharField(max_length=255)
    

    def __str__(self):
        return self.username

     
