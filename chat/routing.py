from django.urls import path, re_path
from . import consumers

# Routing for the ASGI websocket 
websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer, name='chatroom'),
]