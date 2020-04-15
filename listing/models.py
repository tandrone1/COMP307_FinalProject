# Create your models here.
from django.db import models

from datetime import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone
from transaction.models import Transaction

class Listing(models.Model):
    #Change author to correspond to account eventually
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    file_path = models.CharField(max_length=256, null=True)
    text = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    inventory = models.IntegerField(null=True)
    publish_date = models.DateTimeField(default=timezone.now)
    edit_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.edit_date = datetime.now()
        super(Listing, self).save(*args, **kwargs)







class PurchasedListing(models.Model):
    #Change author to correspond to account eventually
    # id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE,default=1)
    author = models.TextField(null=True)
    title = models.TextField(null=True)
    file_path = models.TextField(null=True)
    text = models.TextField(null=True)
    price = models.TextField(null=True)
    #purchaser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(PurchasedListing, self).save(*args, **kwargs)

    @classmethod    
    def create(cls, author, title, file_path, text, price):
        purchasedlisting = cls(author=author, title=title, file_path = file_path, text = text, price = price)
        return purchasedlisting