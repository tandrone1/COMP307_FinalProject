from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from account.models import *


# View for Chat main page 
@login_required
def index(request):

    # Appends all users into the context to show a list of all Bidding Rooms 
    users = []
    for u in User.objects.all():
        users.append({
            'username': u.username
        })

    context = {'users': users}
    context['user'] = request.user

    return render(request, 'chat/index.html', context)

# View for Bidding Rooms 
@login_required
def room(request, room_name=None):

    context = {}
    context['user'] = request.user
    context['room_name'] = room_name
    # The room name should matach an Account, otherwise send empty 
    try:
        context['room_user'] = Account.objects.get(username=room_name)
    except Account.DoesNotExist:
        context['room_user'] = []
    
    return render(request, 'chat/room.html', context)
    