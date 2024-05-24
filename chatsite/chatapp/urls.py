from django.urls import path
from . import views

app_name = 'chatapp'

urlpatterns = [
    path('', views.create_room, name='create-room'),
    path('<str:room_name>/', views.message_view, name='room'),
]