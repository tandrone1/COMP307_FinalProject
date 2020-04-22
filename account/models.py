from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Account holds any additional information for Users (Profile pictures)
class Account(models.Model):
	username = models.CharField(max_length=100, default="")
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	picture = models.CharField(max_length=256, null=True)

	

