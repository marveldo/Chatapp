import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chatmodel,Profile,User,Chatnotification

class FirstConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
       
        userid = self.scope['user'].id
        other_user = self.scope['url_route']['kwargs']['user_id']
        if int(userid) > int(other_user) :
                self.group_name = f'{userid}-{other_user}'
        else:
             self.group_name = f'{other_user}-{userid}'
       
        
        await self.accept()

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.send(json.dumps({
            'type': 'connection-established',
            'message':'connection was succesful'
        }) )
    async def receive(self, text_data):
        
        data_received = json.loads(text_data)
        message = data_received['text']
        username = data_received['username']
        receiver = data_received['otherusername']
        
        await self.message_saved(username, self.group_name,  message, receiver)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'chat' : message,
                'username':username
            }
        )
    async def chat_message(self,event):

        message = event['chat']
        username = event['username']

        await self.send(json.dumps({
            'type' : 'chat',
            'message_sent' : message,
            'username' : username
        }))
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
            
        )
    
    @database_sync_to_async
    def message_saved(self, martins, thread_name, message, receiver):
        otheruser_id = self.scope['url_route']['kwargs']['user_id']
        chat_obj = Chatmodel.objects.create(
              username = self.scope['user'].username,
              thread_name = thread_name,
              message= message
         )
        otheruser = User.objects.get(id = otheruser_id)
        userprofile = Profile.objects.get(user = otheruser)
        if otheruser.username == receiver :
             Chatnotification.objects.create(
                  chat = chat_obj,
                  profile = userprofile,
                  message = f'{self.scope["user"]} sent you a message'

             )
             
        
        
         
class OnlineConsumer(AsyncWebsocketConsumer):
     async def connect(self):
          
          await self.accept()
          self.group_name = 'Friends'

          await self.send(json.dumps({
               'type' : 'useronline',
               'message' : 'online'
          }))
          await self.channel_layer.group_add(
               self.group_name,
               self.channel_name
          )
     async def receive(self, text_data):
          
          data = json.loads(text_data)
          username = data['username']
          status = data['status']
          print(status)
          await self.send(json.dumps({
               'username':username,
               'status':status
          }))

          await self.updateonlinestatus(username,status)
          
     async def disconnect(self, code):
          
          await  self.channel_layer.group_discard(
               self.group_name,
               self.channel_name
          )
      
     @database_sync_to_async
     def updateonlinestatus(self,username,status):
          profile = Profile.objects.get(name = username)
          if status == 'online':
               profile.isonline = True
               profile.save()
          else:
               profile.isonline = False
               profile.save()

class NotifyConsumer(AsyncWebsocketConsumer):

     async def connect(self):
          self.group_name = f'{self.scope["user"].id}'
          await self.channel_layer.group_add(
               self.group_name,
               self.channel_name
          )
          await self.accept()
          await self.send(json.dumps({
               'type':'Notification',
               'print': 'Success connecting!!!'
          }))

     async def get_notification(self,event):
          value = event['value']
          await self.send(json.dumps({
               'type' : 'notification',
               'count': value

          }))


    
     async def disconnect(self, code):
          await self.channel_layer.group_discard(
               self.group_name,
               self.channel_name
          )
     
          
