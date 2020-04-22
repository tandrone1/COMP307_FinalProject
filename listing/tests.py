from django.test import TestCase
from account.forms import *

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
		self.assertTrue(Listing.objects.filter(author=testuser1).exists())
		testuser1.delete()
		self.assertFalse(Listing.objects.filter(author=testuser1).exists())
  
		print('Listing cascade on user delete verified')
  
	def test_forms(self):
		# Tests if the form submit is valid 
		form_data = {'username': 'randomuser', 'password': 'randompass'}
		form = LoginForm(data=form_data)
		self.assertTrue(form.is_valid())
  
		# Tests if the validation response for login is correct (no matching credentials)
		response = self.client.post("/account/login", form_data)
		self.assertFormError(response, 'form', None, 'Incorrect username and password combination')
  
		# Tests if the validation response for signup is correct (email + password errors)
		response = self.client.post("/account/signup", {'username': 'randomuser', 'email': 'test.com', 'password': 'randompass', 'password_confirm': 'randompas'})
		self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
		self.assertFormError(response, 'form', 'password_confirm', 'Passwords do not match.')
  
		print('Form Validation verified')