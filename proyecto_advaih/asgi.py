"""
ASGI config for proyecto_advaih project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_advaih.settings')

# 1. permitir peticiones http

django_asgi_app = get_asgi_application()

#2. permitir canales y websockets
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from usuarios.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    #si la peticion empieza con http:// o htpps://
    "http": django_asgi_app,

    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})
