from django.forms import ModelForm
from .models import Listing

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
        
