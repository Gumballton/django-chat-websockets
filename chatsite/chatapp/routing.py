from django.urls import path
from .consumers import ChatConsumer

websoket_urlpatterns = [
    path('ws/notification/<str:room_name>/', ChatConsumer.as_asgi()),
]