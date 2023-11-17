from django.urls import path
from .consumers import NotificationConsumer

websocket_urls = [
    path('notifs/' , NotificationConsumer.as_asgi())
]