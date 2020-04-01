from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone
from account.models import Account

class Transaction(models.Model):
	customer = models.ForeignKey(Account, on_delete=models.CASCADE)
	date = models.DateTimeField(default=timezone.now)