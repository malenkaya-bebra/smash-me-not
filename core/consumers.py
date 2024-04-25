from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from.models import Post, User, SmashRequest
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass  # Здесь можно добавить логику отключения, если это необходимо

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({'message': event['message']}))

    async def receive(self, text_data):
        data = json.loads(text_data)
        post_id = data.get('post_id')

        if post_id:
            try:
                post = await self.get_post(post_id)
                if post:
                    receiver_id = data.get('receiver_id')
                    if receiver_id:
                        receiver = await self.get_user(receiver_id)
                        if receiver:
                            sender = self.scope['user']
                            smash_request = SmashRequest(post=post, sender=sender, receiver=receiver)
                            smash_request.save()
                            await self.send(text_data=json.dumps({'success': True}))
                        else:
                            await self.send(text_data=json.dumps({'success': False, 'error': 'Invalid receiver_id'}))
                    else:
                        await self.send(text_data=json.dumps({'success': False, 'error': 'receiver_id is required'}))
                else:
                    await self.send(text_data=json.dumps({'success': False, 'error': 'Post not found'}))
            except Post.DoesNotExist:
                await self.send(text_data=json.dumps({'success': False, 'error': 'Invalid post_id'}))
        else:
            await self.send(text_data=json.dumps({'success': False, 'error': 'post_id is required'}))

    @database_sync_to_async
    def get_post(self, post_id):
        return Post.objects.get(pk=post_id)

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(pk=user_id)
