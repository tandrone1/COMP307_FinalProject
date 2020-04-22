from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.files.storage import default_storage
from . import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from transaction.models import Transaction
from listing.models import *
from account.models import *

# View for account profile
@login_required
def profile(request):

    context = {}
    context['user'] = request.user
    context['account'] = Account.objects.get(user=request.user)
    context['my_listings'] = Listing.objects.filter(author=request.user)

    # If the user submits form to change profile picture
    if request.method == "POST":
        file = request.FILES['profile-picture']
        default_storage.save(file.name, file)
        # Set the picture attribute in Account model to the filename of image 
        account = Account.objects.get(user=request.user)    
        account.picture = file.name       
        account.save()
        return redirect('/account')

    else:
        return render(request, 'account/profile.html', context)


# View for signing up 
def signup_action(request):
    context = {}
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            try:
                # User creation using data from form 
              user = User.objects.create_user(
                form.cleaned_data['username'], 
                email=form.cleaned_data['email'], 
                password=form.cleaned_data['password'])
                # Account is a 1-to-1 model with User, stores profile picture 
              account = Account(username=user.username, user=user, picture='default-profile-picture.jpg')
              account.save()

              return HttpResponseRedirect(reverse('login'))
          
            except IntegrityError:
                form.add_error('username', 'Username is taken')

        context['form'] = form   
    return render(request, 'account/signup.html', context)


# View for logging in 
def login_action(request):
    context = {}
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # Attempt to authenticate the user based on credentials 
            user = authenticate(request, 
              username=form.cleaned_data['username'], 
              password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                return HttpResponseRedirect(reverse('listing_list'))
            else:
                # If the user could not be authenticated, propogate error in form 
                form.add_error(None, 'Incorrect username and password combination')
        context['form'] = form
    return render(request, 'account/login.html', context)


# View for logging out 
@login_required
def logout_action(request):
    # Adds a message on redirect to /login to say Logout Complete 
    messages.add_message(request, messages.INFO, 'Logout complete.')

    # If user is logged in another tab while in chat room, will send message to that channel group 
    if request.user.is_authenticated:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(request.user.username, {
            'type': 'logout_message',
            'message': 'Disconnecting. You logged out from another browser or tab.'})

    logout(request)
    return HttpResponseRedirect(reverse('login'))


# View for viewing history 
@login_required
def history_action(request):
    context = {}
    if request.user.is_authenticated:
        # Finds all trasactions from that User
        transactions = Transaction.objects.filter(customer=request.user)
        pl={}
        carts={}
        # Finds all the purchased listings from those transactions 
        for t in reversed(transactions):
            cart = PurchasedListing.objects.filter(transaction=t)
            pl={str(t.date.strftime("%c")):cart}
            carts.update(pl)
        
        context['carts'] = carts
    return render(request, 'account/history.html', context)