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
import json
import string
import random
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied

from django.core.files.storage import default_storage
from django.shortcuts import redirect
from django.core import serializers


# Create your views here.2
#This view gives the list view of the listings
@login_required
def listing_list(request):
    context = {'my_listings': Listing.objects.filter(author=request.user)}
    context['user'] = request.user 
    context['listings'] = Listing.objects.exclude(author=request.user)

    #Use this flush to clear the system after testing
    #Transaction.objects.all().delete()
    itemsincart=[]
    if request.session.get('cart') is None:
        request.session['cart']=json.loads('{}')
        t = Transaction(customer=request.user)
        t.save()
        request.session['transaction'] = t.id
       
        #####

    if request.method == "POST":
        form = PurchasedListingForm(request.POST)
        form2 = PurchasedListingIDForm(request.POST)
        form3 = checkoutForm(request.POST)
        if form.is_valid() and form2.is_valid():

            #creating the purchased listing based on the selected one
            pl = PurchasedListing.create(request.POST.get('author'),request.POST.get('title'),request.POST.get('file_path'),request.POST.get('text'),request.POST.get('price'))
            pl.transaction=Transaction.objects.get(id=request.session['transaction'])
            pl.parent = Listing.objects.get(id=request.POST.get('id'))
            pl.save()
            #getting the cart from session
            cart2 = request.session.get('cart')
            if isinstance(cart2, str):
                cart3 = json.loads(cart2)
            else:
                cart3 = cart2
            isin=True
            while(isin):
                slug = randomString()
                if(slug not in cart3.keys()):
                    isin=False
                    cart3[slug]=pl.id
                    #this is more robust, puts the whole object in the session, above is simpler
                    #cart3[slug]=serializers.serialize("json", PurchasedListing.objects.filter(id=pl.id))
            request.session['cart']=json.dumps(cart3)
            
        #request.POST.get('<thing>') correspons to <input type="hidden" id="<thing>" name="<thing>" value="checkout">
        if request.POST.get('checkInput') is not None:
            print("CHECKOUT" + request.POST.get('checkInput'));

        #handling removing objects from the cart
        if request.POST.get('id') is not None and int(request.POST.get('id')) != -1 and request.POST.get('author') is None:
            print (request.POST.get('id'))
            delkey=None
            #getting the key of the item to be removed
            for i,j in json.loads(request.session.get('cart')).items():
                if j == int(request.POST.get('id')):
                    delkey=i
                    
            #removing the object from the session, and deleting the obect itself
            cart3 = json.loads(request.session.get('cart'))
            del cart3[delkey]
            request.session['cart']=json.dumps(cart3)

            print('deleted:' + str(delkey))
            PurchasedListing.objects.get(id=request.POST.get('id')).delete()

        #handles the management of the cart object
        if request.POST.get('pl') is not None:
            for i in json.loads(request.session.get('cart')).values():
                j = Listing.objects.get(id=(PurchasedListing.objects.get(id=i)).parent.id)
                if j is not None:
                    j.inventory = j.inventory-1
                    j.save()
            request.session['cart']='{}'
            

        print("cart:" + str(request.session['cart']))
        
        if isinstance(request.session.get('cart'),str):
            pequod = json.loads(request.session.get('cart'))
        else:
            pequod = request.session.get('cart')
        for i in pequod.values():
            itemsincart.append(i)


    context['itemcart'] = PurchasedListing.objects.filter(id__in=itemsincart) 

    

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




############################
#HELPER FUNCTIONS
############################
def randomString(stringLength=4):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))



