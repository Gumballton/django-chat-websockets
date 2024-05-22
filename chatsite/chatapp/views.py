from django.shortcuts import redirect, render

from chatapp.models import MessagesModel, RoomModel

# Create your views here.


def create_room(request):
    if request.method == 'POST':
        username = request.POST['username']
        get_room  = request.POST['room']

        try:
            room = RoomModel.objects.get(room_name=get_room)

        except RoomModel.DoesNotExist:
            new_room = RoomModel(room_name=get_room)
            new_room.save()
        
        return redirect('room', username=username, room_name=room)

    return render(request, 'index.html')

def message_view(request, room_name, username):
    get_room = RoomModel.objects.get(room_name=room_name)
    get_messages = MessagesModel.objects.filter(room_name=get_room)

    context =  {
        'room_name': room_name,
        'messages': get_messages,
        'user': username, 
    }

    return render(request, 'message.html', context)