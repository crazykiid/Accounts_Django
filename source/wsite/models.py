from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


# Extended Properties Of User Table
class UserInfo(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  middle_name = models.CharField(max_length=64, blank=True)
  contact = models.CharField(max_length=16, blank=True)
  status = models.IntegerField(default=0)
  
  def __str__(self):
    return str(self.user)
  