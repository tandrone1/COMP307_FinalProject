from django.test import TestCase
from account.forms import *
from django.contrib.auth.models import User
from listing.models import Listing, PurchasedListing, Transaction


# Run python3 manage.py test finalApp to run tests 
class TestCases(TestCase):
    
    # Test to see if PurchasedListing persists purchases after Listings are deleted
	def test_purchasedListing_persistance(self):
        # First create test users and example Listings
		testuser1 = User.objects.create(username='testuser1')
		testuser2 = User.objects.create(username='testuser2')
		testuser1.save()
		testuser2.save()
		l = Listing.objects.create(author=testuser1,title="test",file_path=None,text="Lorem Ipsum",price=10,inventory=10)
		l.save()
        # Next, make a transaction and save it into PurchasedListing
		t = Transaction(customer=testuser2)
		t.save()
		pl = PurchasedListing.objects.create(transaction=t,author=l.author.username,title=l.title,file_path=l.file_path,text=l.text,price=l.price,parent=l)
		pl.save()
		l = Listing.objects.get(title="test")
		pl = PurchasedListing.objects.get(parent=l)
		l.inventory = 0
		l.save()
        # Finally, delete the listing and test if the PurchasedListing object is not none (not-empty)
		l.delete()
		self.assertIsNotNone(pl)
  
		print('PurchasedListing persistence verified')

    # Test to see if deleting user deletes all associated listings
	def test_listing_delete(self):
        # Create test user and a test listing 
		testuser1 = User.objects.create(username='testuser1')
		testuser1.save()
		l = Listing.objects.create(author=testuser1,title="test",file_path=None,text="Lorem Ipsum",price=10,inventory=10)
		l.save()
        # First test to see if the listing exists under that author
		self.assertTrue(Listing.objects.filter(author=testuser1).exists())
        # Then we delete, and see if the listing exists anymore (should not once author deleted)
		testuser1.delete()
		self.assertFalse(Listing.objects.filter(author=testuser1).exists())
  
		print('Listing cascade on user delete verified')
  
    # Test to see if Account form validations work 
	def test_form_validation(self):
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