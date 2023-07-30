from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import uuid



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, blank = True, null = True)
    name = models.CharField(max_length=120, blank = True, null = True)
    profile_pic = models.ImageField( default='images.jpeg' ,upload_to='profiles', blank = True, null = True)
    bio = models.TextField(blank = True, null = True)
    email = models.EmailField(blank = True, null = True)
    isonline = models.BooleanField(default=False, null = True)
    id = models.UUIDField(default= uuid.uuid4, editable= False, unique=True, primary_key=True)

    def __str__(self):
        return self.user.username
    
class Chatmodel(models.Model):
    username = models.CharField(max_length= 120, blank = True, null = True)
    thread_name = models.CharField(max_length = 120, blank = True, null = True )
    message = models.TextField(blank = True, null = True)
    is_read = models.BooleanField(default = False, null = True, blank = True)
    timestamp = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.thread_name
    
class Chatnotification(models.Model):
    chat = models.ForeignKey(Chatmodel, on_delete= models.CASCADE, blank = True, null = True)
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE, blank = True, null = True)
    message = models.TextField(blank = True, null = True)
    is_seen = models.BooleanField(default= False, null = True)

    def __str__(self):
        return self.message





def CreateProfile(sender,instance,created,**kwargs):
    if created:
        user = instance
        Profile.objects.create(
            user = user,
            name = user.username,
            email = user.email
        )


post_save.connect(CreateProfile,sender=User)

def Notification(sender,instance,created,**kwargs):
    if created:
        channel_layer = get_channel_layer()
        notification_count = Chatnotification.objects.filter(is_seen = False, profile = instance.profile).count()
        user_id = str(instance.profile.user.id)
        data = {
            'count': notification_count
        }
        async_to_sync(channel_layer.group_send)(
           user_id,
           {
               'type' : 'get_notification',
               'value':data
           }
        )

post_save.connect(Notification, sender= Chatnotification)