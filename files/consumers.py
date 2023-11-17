import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

topics = {}

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        print(close_code)

    async def receive(self, text_data):
        _message = json.loads(text_data)
        print(text_data)
        if _message and _message.get('type'):
            if _message['type'] == 'subscribe':
                topics_to_subscribe = _message.get('topics', [])
                await self.subscribe(topics_to_subscribe)
            elif _message['type'] == 'unsubscribe':
                topics_to_unsubscribe = _message.get('topics', [])
                await self.unsubscribe(topics_to_unsubscribe)
            elif _message['type'] == 'publish':
                await self.publish(_message)
            elif _message['type'] == 'ping':
                await self.send(text_data=json.dumps({'type': 'pong'}))

    @sync_to_async
    def subscribe(self, topics_to_subscribe):
        for topic_name in topics_to_subscribe:
            subs = topics.get(topic_name, set())
            subs.add(self)
            topics[topic_name] = subs

    @sync_to_async
    def unsubscribe(self, topics_to_unsubscribe):
        for topic_name in topics_to_unsubscribe:
            if topic_name in topics:
                subs = topics[topic_name]
                subs.discard(self)
                if len(subs) == 0:
                    del topics[topic_name]

    @sync_to_async
    def publish(self, _message):
        if _message.get('topic'):
            receivers = topics.get(_message['topic'], set())
            _message['clients'] = len(receivers)
            for receiver in receivers:
                receiver.send(text_data=json.dumps(_message))

