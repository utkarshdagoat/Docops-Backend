import os


from channels.auth import AuthMiddlewareStack

from channels.routing import ProtocolTypeRouter , URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docops.settings')

django_asgi_application = get_asgi_application()

from notifications.routing import websocket_urls

application = ProtocolTypeRouter(
    {
        "http":django_asgi_application,
        "websocket":URLRouter(websocket_urls)
    }
)






