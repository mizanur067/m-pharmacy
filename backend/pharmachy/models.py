from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100,blank=False)
    email = models.EmailField(unique=True,blank=False)
    phone = models.CharField(max_length=15,blank=True)
    password = models.CharField(max_length=100,blank=False)
    failed_login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)


class Staff(models.Model):
    name = models.CharField(max_length=100,blank=False)
    email = models.EmailField(unique=True,blank=False)
    phone = models.CharField(max_length=15,blank=True)
    password = models.CharField(max_length=100,blank=False)
    address = models.TextField(blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)

    