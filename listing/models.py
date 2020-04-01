# Create your models here.
from django.db import models


from django.conf import settings
from django.db import models
from django.utils import timezone

class Listing(models.Model):
	#Change author to correspond to account eventually
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    file_path = models.CharField(max_length=256, null=True)
    text = models.TextField()
    price = models.TextField(null=True)
    inventory = models.TextField(null=True)
    
    # price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    # inventory = models.IntegerField(null=True)
    publish_date = models.DateTimeField(default=timezone.now)
    edit_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.title

	#inventory
