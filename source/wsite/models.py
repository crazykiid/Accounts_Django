from django.db import models

# Create your models here.
class admin_accounts(models.Model):
  _id = models.AutoField(primary_key=True)
  _username = models.CharField(max_length=63, unique=True)
  _password = models.CharField(max_length=255)
  _reg_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self._username


class user_accounts(models.Model):
  _id = models.AutoField(primary_key=True)
  _name = models.CharField(max_length=63)
  _email = models.CharField(max_length=63, unique=True)
  _contact = models.CharField(max_length=10)
  _password = models.CharField(max_length=255)
  _status = models.IntegerField(default=0)
  _reg_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self._name} ({self._email})'