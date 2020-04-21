from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone
from account.models import Account

class Transaction(models.Model):
	customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.date

	def save(self, *args, **kwargs):
		super(Transaction, self).save(*args, **kwargs)