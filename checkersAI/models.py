from django.db import connections
from django.db import models


class Users(models.Model):
    userid = models.CharField(max_length=100)
    userpassword = models.CharField(max_length=100)


class Userstable(models.Model):
    userid = models.CharField(max_length=100)
    userpassword = models.CharField(max_length=100)
    aidifficulty = models.IntegerField()

    class Meta:
        db_table = "usertable"
