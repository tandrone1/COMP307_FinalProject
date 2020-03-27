from django.db import models


from django.conf import settings
from django.db import models
from django.utils import timezone

class Listing(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=256)
	text = models.TextField()
	publish_date = models.DateTimeField(default=timezone.now)
	edit_date = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return self.title

	#inventory

