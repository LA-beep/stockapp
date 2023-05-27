from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ticker = models.CharField(max_length=10, default='AAPL')
    algorithm = models.CharField(max_length=255, default='default_algorithm')
    result = models.TextField(default='0')
    timestamp = models.DateTimeField(auto_now_add=True,null=True,blank=True)
