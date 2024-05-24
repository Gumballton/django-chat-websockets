from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from datetime import timedelta

from chatapp.models import MessagesModel, RoomModel

# Create your views here.

@login_required
def create_room(request):
    if request.method == 'POST':
        room_name  = request.POST['room']

        try:
            room = RoomModel.objects.get(room_name=room_name)
            return redirect('chatapp:room', room_name=room_name)

        except RoomModel.DoesNotExist:
            new_room = RoomModel(room_name=room_name)
            new_room.save()
        
            return redirect('chatapp:room', room_name=room_name)

    return render(request, 'index.html')

@login_required
def message_view(request, room_name):
    get_room = RoomModel.objects.get(room_name=room_name)
    get_messages = MessagesModel.objects.filter(room_name=get_room)

    context =  {
        'room_name': room_name,
        'messages': get_messages,
        'user': request.user,
        'username': request.user.username,
        'current_date': timezone.now(),
        'yesterday': timezone.now() - timedelta(1),
    }

    return render(request, 'message.html', context)