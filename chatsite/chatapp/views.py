from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import timedelta

from chatapp.models import MessagesModel, RoomModel

# Create your views here.


def create_room(request):
    if request.method == 'POST':
        username = request.POST['username']
        get_room  = request.POST['room']

        try:
            room = RoomModel.objects.get(room_name=get_room)
            return redirect('room', username=username, room_name=get_room)

        except RoomModel.DoesNotExist:
            new_room = RoomModel(room_name=get_room)
            new_room.save()
        
            return redirect('room', username=username, room_name=get_room)

    return render(request, 'index.html')

def message_view(request, room_name, username):
    get_room = RoomModel.objects.get(room_name=room_name)
    get_messages = MessagesModel.objects.filter(room_name=get_room)

    context =  {
        'room_name': room_name,
        'messages': get_messages,
        'user': username, 
        'current_date': timezone.now(),
        'yesterday': timezone.now() - timedelta(1),
    }

    return render(request, 'message.html', context)