from cgitb import lookup
from random import randint
from time import sleep
# from .models import IotChannelData
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async



class AIStatusConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = 'iot'
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()  

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)

        value=text_data_json['value']
        name=text_data_json['name']
        dict_type={
                    'type': 'AIControllerBroadCaste',
                }
        res = { **dict_type,**text_data_json,}
       
        # try:
        #      t = await database_sync_to_async(IotChannelData.objects.get)(name=name)
        #      t.value = value 
        #      await database_sync_to_async(t.save)()
        # except:
        #     await database_sync_to_async(IotChannelData.objects.create)(name=name,value=value)


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            res
        )

    # Receive message from room group
    async def AIControllerBroadCaste(self, event):
        print(event)
    # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
            
       