import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # 接受连接
        self.accept()

    def disconnect(self,close_code):
        pass

    def receive(self,text_data):
        '''从套接字接收消息'''
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # 把消息发送给套接字
        self.send(text_data=json.dumps({'message':message}))
