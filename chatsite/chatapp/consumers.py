import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from . import models


class ChatConsumer(AsyncWebsocketConsumer):
    
    """
    Class representing a chat WebSocket connection.

    This class handles WebSocket connections for a chat, including
    receiving new messages, sending them, and saving them to the database.
    """

    async def connect(self) -> None:

        """
        Handler for WebSocket connection event.

        Establishes a connection to the chat room group and accepts the connection.

        """

        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name'].replace(' ', '_')}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code: int) -> None:

        """
        Handler for WebSocket disconnection event.

        Removes the connection from the chat room group.
        """

        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data: str) -> None:

        """
        Handler for receiving a message via WebSocket.

        Unpacks the JSON message and sends it to the chat room group.
        """

        text_data_json = json.loads(text_data)
        message = text_data_json

        event = {
            'type': 'send_message',
            'message': message,
        }
        
        await self.channel_layer.group_send(self.room_name, event)

    async def send_message(self, event: dict) -> None:

        """
        Handler for sending a message to the chat room group.

        Creates a new message based on the event data and sends it
        to the chat room group, and also saves it to the database.
        """

        data = event['message']
        await self.create_message(data=data)
        response_data = {
            'sender': data['sender'],
            'message': data['message'],
        }

        await self.send(text_data=json.dumps({'message': response_data}))

    @database_sync_to_async
    def create_message(self, data: dict) -> None:

        """
        Asynchronous method for creating a new message in the database.

        Finds the room by name, creates a new message, and saves it
        to the database if such a message does not already exist.
        """

        get_room_by_name = models.RoomModel.objects.get(room_name=data['room_name'])
        if not models.MessagesModel.objects.filter(message=data['message']).exists():
            new_message = models.MessagesModel(room_name=get_room_by_name,
                                               sender=data['sender'],
                                               message=data['message'])
            new_message.save()