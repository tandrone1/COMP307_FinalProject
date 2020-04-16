from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# account holds any additional information for Users (Profile pictures)
class Account(models.Model):
	username = models.CharField(max_length=100, default="delete")
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	picture = models.CharField(max_length=256, null=True)

	

