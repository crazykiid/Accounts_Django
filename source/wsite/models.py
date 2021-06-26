from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.

class UserInfo(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  contact = models.IntegerField()
  status = models.IntegerField(default=0)
  
  def __str__(self):
    return str(f'{self.user}')
  