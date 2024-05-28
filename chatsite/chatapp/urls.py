from django.urls import path
from . import views

app_name = 'chatapp'

urlpatterns = [
    path('', views.MainPageView.as_view(), name='mainpage'),
    path('create/', views.create_room, name='create-room'),
    path('enter/', views.enter_room, name='enter-room'),
    path('<str:room_name>/', views.message_view, name='room'),
    path('delete_chat/<int:room_id>/', views.delete_chat, name='delete_chat'),
]