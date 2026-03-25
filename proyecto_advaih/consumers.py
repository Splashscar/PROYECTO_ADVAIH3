from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificacionConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = "notificaciones"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def enviar_notificacion(self, event):
        await self.send(text_data=json.dumps({
            "mensaje": event["mensaje"]
        }))
