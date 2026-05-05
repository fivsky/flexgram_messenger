import json
import os
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile
from django.conf import settings
from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_slug = self.scope['url_route']['kwargs']['room_slug']
        self.room_group_name = f'chat_{self.room_slug}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            result = await self.save_file(bytes_data)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_file',
                    'file_url': result['file_url'],
                    'file_name': result['file_name'],
                    'file_type': result['file_type'],
                    'username': self.scope['user'].username,
                }
            )
        else:
            data = json.loads(text_data)
            message = data.get('message', '')
            await self.save_message(self.scope['user'], self.room_slug, message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': self.scope['user'].username,
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'username': event['username'],
        }))

    async def chat_file(self, event):
        await self.send(text_data=json.dumps({
            'type': 'file',
            'file_url': event['file_url'],
            'file_name': event['file_name'],
            'file_type': event['file_type'],
            'username': event['username'],
        }))

    @database_sync_to_async
    def save_message(self, user, room_slug, message):
        room = Room.objects.get(slug=room_slug)
        Message.objects.create(user=user, room=room, content=message)

    @database_sync_to_async
    def save_file(self, bytes_data):
        room = Room.objects.get(slug=self.room_slug)
        msg = Message.objects.create(
            user=self.scope['user'],
            room=room,
            content='',
        )

        header = bytes_data[:12]
        ext = '.bin'
        file_type = 'other'

        # Изображения
        if header.startswith(b'\xff\xd8\xff'):
            ext = '.jpg';
            file_type = 'image'
        elif header.startswith(b'\x89PNG\r\n\x1a\n'):
            ext = '.png';
            file_type = 'image'
        elif header.startswith(b'GIF8'):
            ext = '.gif';
            file_type = 'image'
        elif header.startswith(b'RIFF') and b'WEBP' in header:
            ext = '.webp';
            file_type = 'image'
        # Видео
        elif header[4:8] == b'ftyp':  # mp4
            ext = '.mp4';
            file_type = 'video'
        elif header[:4] == b'\x1a\x45\xdf\xa3':  # webm
            ext = '.webm';
            file_type = 'video'

        # Аудио
        elif len(header) >= 4 and header[0:4] == b'\x1aE\xdf\xa3':  # webm (может быть аудио)
            ext = '.webm'
            file_type = 'audio'  # считаем аудио, если запись только звука
        elif header.startswith(b'OggS'):
            ext = '.ogg'
            file_type = 'audio'

        # Документы
        elif header.startswith(b'%PDF'):
            ext = '.pdf';
            file_type = 'document'
        elif header.startswith(b'PK\x03\x04'):
            ext = '.zip';
            file_type = 'archive'

        file_name = f'file_{msg.id}{ext}'
        msg.file.save(file_name, ContentFile(bytes_data))
        msg.save()

        return {
            'file_url': settings.MEDIA_URL + str(msg.file),
            'file_name': file_name,
            'file_type': file_type,
        }
