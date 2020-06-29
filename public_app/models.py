from django.db import models
from django.contrib.auth.models import User

class User_Detail(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, blank = True, null= True)
    
class Jobs(models.Model):
    title = models.CharField(max_length=600, blank = True, null= True)
    body = models.TextField()
