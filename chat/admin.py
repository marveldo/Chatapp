from django.contrib import admin
from .models import Profile,Chatmodel,Chatnotification
# Register your models here.
admin.site.register(Profile)
admin.site.register(Chatmodel)
admin.site.register(Chatnotification)