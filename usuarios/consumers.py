import json
from channels.generic.websocket import AsyncWebsocketConsumer
from proyecto_advaih.Firebase_config import initialize_firebase
from firebase_admin import firestore
from asgiref.sync import sync_to_async

db = initialize_firebase()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "adso_chat_global"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, class_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        mensaje = data["mensaje"]
        uid_usuario = ["usuario"]

        #1. guardar en forestore el mensaje
        await self.guardar_mensaje_firestore(uid_usuario, mensaje)

        #2. emitir el mensaje
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type' : 'chat_message',
                'mensaje' : mensaje,
                'usuario' : uid_usuario
            }
        )


        async def chat_message(self, event):
            await self.send(text_data = json.dumps([
                'mensaje' : event
            ]))

        
        