from django.db import models

class user(models.Model):
    email = models.CharField(max_length=40)
    fname = models.CharField(max_length=40)
    lname = models.CharField(max_length=40)
    phone = models.CharField(max_length=10)
    pwd = models.CharField(max_length=40)