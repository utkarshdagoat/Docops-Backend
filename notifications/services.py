from django.conf import settings
from redis import asyncio as aioredis
import redis
from typing import Callable , AsyncGenerator  , Any
import json

def get_async_redis_client():
    try:
        return aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            encoding='utf8',
            decode_responses=True
        )
    except redis.exceptions.ConnectionError as e:
        print("Connection Error:" , e )
    except Exception as e:
        print('An unexpected Error has Occured')


async def listen_to_channel(filter_func: Callable, user_id: int) -> AsyncGenerator:
    r = await redis.asyncio.from_url('redis://localhost:6379')
    async with r.pubsub() as pubsub:
        await pubsub.subscribe('request-notifs')
        print('Subscribed to channel: request-notifs')
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message is not None:
                data = message["data"].decode('utf-8')
                parsed_data = json.loads(data)
                if filter_func(user_id, parsed_data):
                    yield f"data: {json.dumps(parsed_data)}\n\n"

def is_user_recipient(user_id:int , message:dict[str,Any]) -> bool:
    return str(user_id) == message.get('recipient_id')


