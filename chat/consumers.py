from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import ChatMessage
from StudentApp.models import *


class ChatConsumer(AsyncWebsocketConsumer):
    order=None

    async def connect(self):
        print("WebSocket connected")  
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.order = await self.get_order_instance(self.order_id)
        
        await self.channel_layer.group_add(
            f"chat_{self.order_id}",
            self.channel_name
        )
        await self.accept()

        existing_messages = await self.get_existing_messages()
        for message in existing_messages:
            await self.send(text_data=json.dumps({
                'message': message['message'],
            }))
            print(message)



    @database_sync_to_async
    def get_existing_messages(self):
        messages = ChatMessage.objects.filter(order=self.order)
        return [{'message': message.message} for message in messages]
      



    async def disconnect(self, close_code):
        print("WebSocket disconnected") 
        await self.channel_layer.group_discard(
            f"chat_{self.order_id}",
            self.channel_name
        )


    async def receive(self, text_data):
        # print("Received message:", text_data)  
        data = json.loads(text_data)
        message = data.get('message', '') 
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        order_id = data.get('order_id')
        await self.save_message(sender_id, receiver_id, order_id, message)

        await self.channel_layer.group_send(
             f"chat_{self.order_id}",
            {
                'type': 'chat_message',
                'message': message,
                'sender':sender_id
            }
        )


    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'sender':sender,
        }))



    @sync_to_async
    def save_message(self, sender_id, receiver_id, order_id,message):
        ChatMessage.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            order_id=order_id,
            message=message
        )


    @database_sync_to_async
    def get_order_instance(self, order_id):
        try:
            order = Orders.objects.get(id=order_id)
            return order
        except Orders.DoesNotExist:
            print("Failed to find the order")