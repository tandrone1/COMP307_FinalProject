from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer



@login_required
def index(request):
    return render(request, 'chat/index.html', {'user': request.user})

@login_required
def room(request, room_name=None):

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'user': request.user
    })
    