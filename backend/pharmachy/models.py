from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100,blank=False)
    email = models.EmailField(unique=True,blank=False)
    phone = models.CharField(max_length=15,blank=True)
    password = models.CharField(max_length=100,blank=False)

    