from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from channels.auth import get_user, logout
from django.contrib.auth.models import User
from account.models import Account

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        user = self.scope['user']
        if user.is_authenticated:
          async_to_sync(self.channel_layer.group_add)(
              user.username,
              self.channel_name
          )

        self.accept()

        if user.is_authenticated:
            message = 'has entered the room.'
        else:
            message = 'Anonymous: ' + ' has entered the room.'
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'message_type': 'meta',
                'user': user.username
            }
        )

    def disconnect(self, close_code):
        # Leave room group
        message = ' has left the room.'

        async_to_sync(self.channel_layer.group_send)(
            
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'message_type': 'meta',
                'user': self.scope['user'].username
            }
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']
        
        if user.is_authenticated:
            message = message
        else:
            message = 'Anonymous: ' + message
            
        try:
            account = Account.objects.get(username=user)
            user_picture = account.picture
        except Account.DoesNotExist:
            user_picture = 'default-profile-picture.jpg'
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'message_type': 'default',
                'user': user.username,
                'user_picture': user_picture
            }
        )
    
    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        message_type = event['message_type']
        user = event['user']
        if message_type == 'meta':
            user_picture = 'default-profile-picture.jpg'
        else:
            user_picture = event['user_picture']
            
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'type': message_type,
            'user': user,
            'user_picture': user_picture
        }))
    
    # Receive message from username group - when you logout from another tab 
    def logout_message(self, event):
        self.send(text_data=json.dumps({
            'message': event['message'],
            'type': 'meta',
            'user': ''
        }))
        self.close()
