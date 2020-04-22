from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.html import escape
from django.utils import timezone
from datetime import datetime
from django.template import Context, Template
from .forms import *
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
from django.contrib import messages



#PROBLEM: IS_LISTING DOES NOT RETURN DUPLICATES LIKE IT SHOULD, PROBLEM IS WITH QUERYSETS WHICH BY DEFAULT CANT BE CHANGED AND DONT HAVE DUPLCIATES
@login_required
def checkout_action(request):
	template = 'transaction/checkout.html'
	IS_Listings = {}
	#sending the lists of purchased and out of stock items
	context = {
		'OOS_Listings':Listing.objects.filter(id__in = request.session.get('bads')),
		'IS_Listings':Listing.objects.filter(id__in = request.session.get('goods'))}
	if request.method == 'POST':
		form = checkoutForm(request.POST)
		if request.POST.get('buy') is not None and form.is_valid():
			#creating the transaction for the checkout
			t = Transaction(customer=request.user)
			t.save()
			#for each item being bought, decrement its inventory by 1
			for j in request.session.get('goods'):
				i = Listing.objects.get(id=j)
				i.inventory = i.inventory-1
				i.save()
				messages.add_message(request, messages.INFO, str(i.title) + " was purchased.")
				#create the new purchasedlisting and attach it
				tempPL = PurchasedListing(transaction=t, author = i.author, title = i.title, file_path = i.file_path, text = i.text, price = i.price, parent = i)
				tempPL.save()
				template = 'listing/listing_list.html'
				context = {'my_listings': Listing.objects.filter(author=request.user)}
				context['user'] = request.user 
				context['listings'] = Listing.objects.exclude(author=request.user)


	return render(request, template, context)
