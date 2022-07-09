from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.
class User(AbstractUser):
    reputation = models.IntegerField(default = 0)

class Owned(models.Model):
    owner = models.CharField(max_length = 20)
    symbol = models.CharField(max_length = 5)
    pricebought = models.FloatField(default = 0)
    shares= models.PositiveIntegerField(default = 0)
    totalprice = models.FloatField(default = 0)
    currentprice = models.FloatField(default = 0)