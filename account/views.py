from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.files.storage import default_storage
from . import forms
from django.shortcuts import redirect
from account.models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib import messages
from transaction.models import Transaction
from listing.models import *

# LEAVE IN CASE WE NEED TO EDIT PERMISSIONS 
# def set_permissions(user):

#     permission = Permission.objects.get(name='Can change listings')
#     permission1 = Permission.objects.get(name='Can delete listings')
#     permission2 = Permission.objects.get(name='Can view listings')
#     user.user_permissions.remove(permission, permission1)
#     user.user_permissions.add(permission2)

@login_required
def profile(request):
    
    context = {}
    context['user'] = request.user
    context['account'] = Account.objects.get(user=request.user)
    context['my_listings'] = Listing.objects.filter(author=request.user)

    if request.method == "POST":
        file = request.FILES['profile-picture']
        default_storage.save(file.name, file)
        
        account = Account.objects.get(user=request.user)    
        account.picture = file.name       
        account.save()
        return redirect('/account')

    else:
        return render(request, 'account/profile.html', context)


def signup_action(request):
    context = {}
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            try:
                # user creation
              user = User.objects.create_user(
                form.cleaned_data['username'], 
                email=form.cleaned_data['email'], 
                password=form.cleaned_data['password'])
                
              account = Account(username=user.username, user=user, picture='default-profile-picture.jpg')
              account.save()

              return HttpResponseRedirect(reverse('login'))
            except IntegrityError:
                form.add_error('username', 'Username is taken')

        context['form'] = form   
    return render(request, 'account/signup.html', context)


def login_action(request):
    context = {}
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, 
              username=form.cleaned_data['username'], 
              password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                return HttpResponseRedirect(reverse('listing_list'))
            else:
                form.add_error(None, 'Incorrect username and password combination')
        context['form'] = form
    return render(request, 'account/login.html', context)

@login_required
def logout_action(request):
    messages.add_message(request, messages.INFO, 'Logout complete.')

    if request.user.is_authenticated:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(request.user.username, {
            'type': 'logout_message',
            'message': 'Disconnecting. You logged out from another browser or tab.'})

    logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required
def history_action(request):
    context = {}
    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(customer=request.user)
        pl={}
        carts={}
        for t in transactions:
            # print(t.id)
            cart = PurchasedListing.objects.filter(transaction=t)
            pl={str(t.date.strftime("%c")):cart}
            carts.update(pl)
        
        context['carts'] = carts
        print(context)
    return render(request, 'account/history.html', context)