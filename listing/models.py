# Create your models here.
from django.db import models

from datetime import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone
from transaction.models import Transaction

import smtplib

from email.mime.text import MIMEText


#####################
#HELPER METHODS#
#####################
def send_simple_message(email, item):
    msg = MIMEText(str(item) + " has run out of stock!")
    msg['Subject'] = str(item) + " has run out of stock!"
    msg['From']    = "ArtSellers@sandboxac000a2cf402486fada60bc179bb0aef.mailgun.org"
    #msg['To']      = email
    msg['To']      = "benicetothem@gmail.com"
    s = smtplib.SMTP('smtp.mailgun.org', 587)
    s.login('postmaster@sandboxac000a2cf402486fada60bc179bb0aef.mailgun.org', '4f2cc1a0febe063c086252e17888c903-f135b0f1-766b5f08')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
    print('sent email to ' + str(email) + " regarding " + str(item) + " being out of stock")



#REAL METHODS#
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
        ####COMMENTED OUT SINCE WE ONLY HAVE 5000 EMAILS!!!###
        # if self.inventory <= 0:
        #     send_simple_message(self.author.email,self.title)
        super(Listing, self).save(*args, **kwargs)


class PurchasedListing(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE,default=1)
    author = models.TextField(null=True)
    title = models.TextField(null=True)
    file_path = models.TextField(null=True)
    text = models.TextField(null=True)
    price = models.TextField(null=True)
    parent = models.ForeignKey(Listing, on_delete=models.SET_NULL, default=None, null=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(PurchasedListing, self).save(*args, **kwargs)

    @classmethod    
    def create(cls, author, title, file_path, text, price):
        purchasedlisting = cls(author=author, title=title, file_path = file_path, text = text, price = price)
        return purchasedlisting


