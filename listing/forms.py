from django.forms import ModelForm
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
        fields = ['author', 'title', 'file_path', 'text', 'price']
