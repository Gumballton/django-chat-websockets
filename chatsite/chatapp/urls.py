from django.urls import path
from . import views



urlpatterns = [
    path('', views.create_room, name='create-room'),
    path('<str:room_name>/<str:username>/', views.message_view, name='room'),
]