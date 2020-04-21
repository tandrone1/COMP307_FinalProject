from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.html import escape
from django.utils import timezone
from datetime import datetime
from .forms import ListingForm, EditListingForm, PurchasedListingForm, PurchasedListingIDForm, checkoutForm
from django.template import Context, Template
from listing.models import *
from transaction.models import *
from account.models import *
import json
import string
import random
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied

from django.core.files.storage import default_storage
from django.shortcuts import redirect
from django.core import serializers
from django.contrib import messages
import requests



# Create your views here.2
#This view gives the list view of the listings
@login_required
def listing_list(request):
    

    context = {'my_listings': Listing.objects.filter(author=request.user)}
    context['listings'] = Listing.objects.exclude(author=request.user)
    template = 'listing/listing_list.html'

    #checks if the checkout button was pushed
    if request.method == "POST":
        form3 = checkoutForm(request.POST)

        #if the button was pressed then move to gathering data    
        if request.POST.get('checkInput') is not None and form3.is_valid():
            print("CHECKOUT" + request.POST.get('checkInput'));
            bads = []
            goods = []
            cart = request.POST.get('checkInput').split(",")
            for i in cart:

                temp = Listing.objects.get(id=i)
                #creating lists of items that were purchased, and failed to be purchased
                if temp.inventory > 0:
                    goods.append(i)
                else:
                    bads.append(i)

 
                
            request.session['bads']=bads
            request.session['goods']=goods
            return redirect('/transaction/checkout')

    return render(request, template, context)


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




############################
#HELPER FUNCTIONS
############################
def randomString(stringLength=4):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))



