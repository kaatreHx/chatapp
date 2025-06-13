from channels.consumer import SyncConsumer, AsyncConsumer
from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('Websocket connect .. ', event)
        print('Channel layer ...', self.channel_layer)
        print('Channel name ...', self.channel_name)
        async_to_sync(self.channel_layer.group_add)('programmers', self.channel_name)
        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print('Message received from client .. ', event['text'])
        print('Type of Message received from client .. ', type(event['text']))
        async_to_sync(self.channel_layer.group_send)('programmers', {
            'type': 'chat.message',
            'message': event['text']
        })
    
    def chat_message(self, event):
        print('Event .. ', event)
        print('Actual Data .. ', event['message'])
        print('Type of Actual Data .. ', type(event['message']))
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    def websocket_disconnect(self, event):
        print('Websocket disconnect .. ', event)
        print('Channel layer ...', self.channel_layer)
        print('Channel name ...', self.channel_name)
        async_to_sync(self.channel_layer.group_discard)('programmers', self.channel_name)
        raise StopConsumer()

class MySyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('Websocket connect .. ', event)
        print('Channel layer ...', self.channel_layer)
        print('Channel name ...', self.channel_name)
        self.channel_layer.group_add('programmers', self.channel_name)
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('Message received from client .. ', event['text'])
        print('Type of Message received from client .. ', type(event['text']))
        await self.channel_layer.group_send('programmers', {
            'type': 'chat.message',
            'message': event['text']
        })
    
    async def chat_message(self, event):
        print('Event .. ', event)
        print('Actual Data .. ', event['message'])
        print('Type of Actual Data .. ', type(event['message']))
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    async def websocket_disconnect(self, event):
        print('Websocket disconnect .. ', event)
        print('Channel layer ...', self.channel_layer)
        print('Channel name ...', self.channel_name)
        await self.channel_layer.group_discard('programmers', self.channel_name)
        raise StopConsumer()