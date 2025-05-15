from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser): 
    birth_date = models.DateField()
    locality = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)


