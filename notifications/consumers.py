from time import sleep
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async


import redis
import json
from .models import Notification
from .serializers import NotificationSerializer

from spaces.models.request import Request

from files.models.request import Request as FileRequest

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self , text_data=None):
        message = json.loads(text_data)
        try:
            try:
                self.user = message['data']['user']
            except KeyError:
                self.user = 'utkarsh_s@ece.iitr.ac.in' 
            r = await redis.asyncio.from_url('redis://localhost:6379')
            async with r.pubsub() as pubsub:
                await pubsub.subscribe('request-notifs')
                while True:
                    message = await pubsub.get_message(ignore_subscribe_messages=True)
                    if message is not None:
                        data = message['data'].decode('utf-8')
                        data_dict = json.loads(data)
                        data_serialized = await self.create_notification(
                            request_id=data_dict['instance_id'] , 
                            notif_type=data_dict['notif_type']
                        )
                        data = json.dumps(data_serialized)
                        if data_serialized['serialized_object']['creator']['email'] == self.user :
                            print('sending to'  , self.user)
                            await self.send_json(data)
        except KeyError:
            pass


    @database_sync_to_async
    def create_notification(self , request_id , notif_type):
        if notif_type == 0:
            print('Creating notification .....')
            request = Request.objects.get(id=request_id)
            message = f"{request.from_user.username} has requested to join {request.space.name}"
            print(message)
            notifcation = Notification(message=message , recipent=request.creator , notif_type=notif_type ,content_object=request)
            notifcation.save()
        else :
            print('Creating notification .....')
            request = FileRequest.objects.get(id=request_id)
            message = f"{request.from_user.username} has requested to edit the file titled {request.file.heading}"
            print(message)
            notifcation = Notification(message=message , recipent=request.file.createdBy , notif_type=notif_type ,content_object=request)
            notifcation.save()
        serializer = NotificationSerializer(notifcation)
        return serializer.data
                    


