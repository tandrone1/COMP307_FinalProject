from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from django.contrib.auth.models import User



@login_required
def index(request):

    users = []
    
    for u in User.objects.all():
        users.append({
            'username': u.username
        })

    context = {'users': users}
    context['user'] = request.user

    return render(request, 'chat/index.html', context)

@login_required
def room(request, room_name=None):

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'user': request.user
    })
    