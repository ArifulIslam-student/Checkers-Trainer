from django.db import connections
from django.db import models


class Users(models.Model):
    userid = models.CharField(max_length=100)
    userpassword = models.CharField(max_length=100)
