from django.urls import re_path
from .consumers import FirstConsumer,OnlineConsumer,NotifyConsumer

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<user_id>\d+)/$', FirstConsumer.as_asgi()),
    re_path(r'ws/online/',OnlineConsumer.as_asgi()),
    re_path(r'ws/notification/', NotifyConsumer.as_asgi())
]