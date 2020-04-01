from django.db import models

# Create your models here.

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Account(models.Model):
	owner = models.OneToOneField(User, on_delete=models.CASCADE)