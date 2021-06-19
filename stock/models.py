from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    reputation = models.IntegerField(default = 0)

class Predictions(models.Model):
    owner = models.CharField(max_length = 20)
    symbol = models.CharField(max_length = 5)
    predictedprice = models.FloatField(default = 0)
    timeposted = models.DateField()
    predictedtime = models.DateField()
    upvotes = models.IntegerField(default = 0)