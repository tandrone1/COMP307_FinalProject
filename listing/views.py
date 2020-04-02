from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.html import escape
from django.utils import timezone
from datetime import datetime
from .forms import ListingForm, EditListingForm
from django.template import Context, Template
from listing.models import *

from django.core.files.storage import default_storage
from django.shortcuts import redirect

# Create your views here.2

#This view gives the list view of the listings
@login_required
def listing_list(request):

    context = {'listings': Listing.objects.all()}
    # listings = []
    # for l in Listing.objects.all():
    #     listings.append({
    #       'title': l.title,
    #       'text': l.text,
    #       'file_path': l.file_path
    #     })
    # context = {'listings': listings}

    return render(request, 'listing/listing_list.html', context)



#This view is for the form to create new listings 
@login_required
def create_listing(request):

    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            file = request.FILES['image']
            default_storage.save(file.name, file)
            listing = form.save(commit=False)
            listing.author = request.user
            listing.file_path = file.name
            listing.publish_date = timezone.now()
            listing.save()
            return redirect('/')
    else:
        form = ListingForm()
    return render(request, 'listing/create_listing.html', {'form': form})



def edit_listing(request, listing_id=None):

    if request.method == "POST":
        context = {}
        form = ListingForm(request.POST)
        context['form'] = form

        if form.is_valid():

            article = Listing.objects.get(id=listing_id)

            listing = ListingForm(request.POST, instance=article)
            
            listing.save(commit=False)
            
            #Edit_date is not changing 
            listing.edit_date = datetime.now()
            listing.save()

            return redirect('/')

    else:
        # Gets the matching listing based on listing_id, gets the form and puts into context
        listings = Listing.objects.filter(id=listing_id)
        if not listings:
            return HttpResponseNotFound('<h3>Page not found.</h3>')
        listing = listings[0]

        context = {'listing': listing}
    
       
    return render(request, 'listing/edit_listing.html', context)


