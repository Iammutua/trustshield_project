from django.db import models

# Create your models here.

class Client(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.IntegerField()
    password = models.CharField(max_length=255)
    date_joined = models.DateField(auto_now_add=True)