import asyncio
from celery import shared_task
from .models import Request
from files.models.request import Request as FileRequest
import redis
from celery.contrib import rdb

import json

@shared_task
def send_notification_request(request_id , notif_type):
    if notif_type == 0:
        instance = Request.objects.get(pk=request_id)
    else:
        instance = FileRequest.objects.get(pk=request_id)
    loop = asyncio.get_event_loop() 
    loop.run_until_complete(publish_to_redis(instance_id=instance.id , notif_type=notif_type))


async def publish_to_redis(instance_id:int , notif_type:int):
    print('publshing to redis...')
    r = await redis.asyncio.from_url('redis://localhost:6379')
    data = {
        "instance_id":instance_id,
        "notif_type":notif_type
    }
    print(data)
    await r.publish('request-notifs', json.dumps(data))
    await r.close()
