import json
#from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone

#class ChatConsumer(WebsocketConsumer):
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'
        # 加入群聊
        #async_to_sync(self.channel_layer.group_add)(
            #self.room_group_name,
            #self.channel_name
        #)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # 接受连接
        await self.accept()

    async def disconnect(self,close_code):
        # 退出群聊
        #async_to_sync(self.channel_layer.group_discard)(
            #self.room_group_name,
            #self.channel_name
        #)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self,text_data):
        '''从套接字接收消息'''
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        # 把消息发送给套接字
        #self.send(text_data=json.dumps({'message':message}))
        # 把消息发到聊天群里
        #async_to_sync(self.channel_layer.group_send)(
            #self.room_group_name,
            #{
                #'type':'chat_message',
                #'message':message,
                #'user':self.user.username,
                #'datetime':now.isoformat(),
            #}
        #)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'user':self.user.username,
                'datetime':now.isoformat(),
            }
        )
    
    async def chat_message(self,event):
        '''向套接字发送消息'''
        await self.send(text_data=json.dumps(event))