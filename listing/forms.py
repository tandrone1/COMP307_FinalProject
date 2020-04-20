from django.forms import ModelForm
from django import forms
from .models import Listing, PurchasedListing

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        # fields = ['title', 'text']
        fields = ['title', 'text', 'price', 'inventory']
        


class EditListingForm(ModelForm):
    class Meta:
        model = Listing
        # fields = ['title', 'text']
        fields = ['title', 'text', 'price', 'inventory']
        

class PurchasedListingForm(ModelForm):
    class Meta:
        model = PurchasedListing
        # fields = ['title', 'text']
        fields = ['id', 'author', 'title', 'file_path', 'text', 'price']

class PurchasedListingIDForm(ModelForm):
    class Meta:
        model = PurchasedListing
        # fields = ['title', 'text']
        fields = ['id']

class checkoutForm(forms.Form):
	checkInput = forms.CharField(label='checkInput', max_length=100)