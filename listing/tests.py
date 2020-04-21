from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from .models import Listing, PurchasedListing, Transaction

class TestCase1(TestCase):
	def test_1(self):
		testuser1 = User.objects.create(username='testuser1')
		testuser2 = User.objects.create(username='testuser2')
		testuser1.save()
		testuser2.save()
		l = Listing.objects.create(author=testuser1,title="test",file_path=None,text="Lorem Ipsum",price=10,inventory=10)
		l.save()
		t = Transaction(customer=testuser2)
		t.save()
		pl = PurchasedListing.objects.create(transaction=t,author=l.author.username,title=l.title,file_path=l.file_path,text=l.text,price=l.price,parent=l)
		pl.save()
		l = Listing.objects.get(title="test")
		pl = PurchasedListing.objects.get(parent=l)
		l.inventory = 0
		l.save()
		l.delete()
		self.assertIsNotNone(pl)
		print('PurchasedListing persistence verified')

	def test_2(self):
		testuser1 = User.objects.create(username='testuser1')
		testuser1.save()
		l = Listing.objects.create(author=testuser1,title="test",file_path=None,text="Lorem Ipsum",price=10,inventory=10)
		l.save()
		testuser1.delete()
		print(l)
		self.assertIsNone(l)
