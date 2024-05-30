from django.urls import path
from .consumers import ChatConsumer

# WebSocket URL patterns for handling WebSocket connections
websoket_urlpatterns = [
    path('ws/notification/<str:room_name>/', ChatConsumer.as_asgi()),
]