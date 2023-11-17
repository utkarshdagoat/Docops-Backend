from django.urls import path
from files.consumers import MyConsumer 
websocket_urls = [
    path("y-webrtc/", MyConsumer.as_asgi()),
]
