from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.html import escape
from django.utils import timezone
from .forms import ListingForm
from listing.models import *

from django.core.files.storage import default_storage

# Create your views here.

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
def create_listing(request):

    context = {'listings': Listing.objects.all()}
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():

            file = request.FILES['image']
            default_storage.save(file.name, file)
            list = form.save(commit=False)
            list.author = request.user
            list.file_path = file.name
            list.save()
            return HttpResponseRedirect('/')
        context['form'] = form

    return render(request, 'listing/create_listing.html', {})