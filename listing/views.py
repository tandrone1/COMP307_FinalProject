from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.html import escape
from django.utils import timezone
from datetime import datetime
from .forms import ListingForm, EditListingForm, PurchasedListingForm
from django.template import Context, Template
from listing.models import *

from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied

from django.core.files.storage import default_storage
from django.shortcuts import redirect

# Create your views here.2
#This view gives the list view of the listings
cart=[]
@login_required
def listing_list(request):
    context = {'my_listings': Listing.objects.filter(author=request.user)}
    context['user'] = request.user 
    context['listings'] = Listing.objects.exclude(author=request.user)

    if request.method == "POST":
        form = PurchasedListingForm(request.POST)
        if form.is_valid():


            #for checking out
            #currently breaks by way of 'cart is not defined before it is used for some reason'
            # if request.POST.get('Buy')=="Buy":
            #     print('items bought')
            #     for i in cart:
            #         i.delete()
            #     cart=[]


            pl = PurchasedListing.create(request.POST.get('author'),request.POST.get('title'),request.POST.get('file_path'),request.POST.get('text'),request.POST.get('price'),request.user)
            cart.append(pl)
            print(cart)

    

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
            listing.edit_date = timezone.now()
            listing.save()
            return redirect('/')
    else:
        form = ListingForm()
    return render(request, 'listing/create_listing.html', {'form': form})


@login_required
def edit_listing(request, listing_id=None):

    if request.method == "POST":
        context = {}
        form = ListingForm(request.POST)
        context['form'] = form

        if form.is_valid():

            article = Listing.objects.get(id=listing_id)

            # Checks if the author of the listing being edited matches the user making the edit 
            if 'edit' in request.POST and request.user == article.author:

                listing = ListingForm(request.POST, instance=article)           
                listing.save(commit=False)
                listing.save()

            elif 'delete' in request.POST and request.user == article.author:

                article = Listing.objects.get(id=listing_id)
                article.delete()

            return redirect('/')

    else:
        # Gets the matching listing based on listing_id, gets the form and puts into context
        listings = Listing.objects.filter(id=listing_id)
        if not listings:
            return HttpResponseNotFound('<h3>Page not found.</h3>')
        listing = listings[0]

        context = {'listing': listing}
        context['user'] = request.user
       
    return render(request, 'listing/edit_listing.html', context)


