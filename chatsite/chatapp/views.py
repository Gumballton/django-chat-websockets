from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib import messages
from django.db import models


from datetime import timedelta

from chatapp.models import MessagesModel, RoomModel
from .forms import RoomCreateForm, RoomEnterForm

# Create your views here.

@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomCreateForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.owner = request.user
            room.save()
            return redirect('chatapp:room', room_name=room.room_name)
    else:
        form = RoomCreateForm()

    return render(request, 'chatapp/index.html', {'form': form, 'title': 'Create Room'})

@login_required
def enter_room(request):
    if request.method == 'POST':
        form = RoomEnterForm(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data['room_name']
            room = RoomModel.objects.get(room_name=room_name)
            room.members.add(request.user)
            return redirect('chatapp:room', room_name=room_name)
    else:
        form = RoomEnterForm()

    return render(request, 'chatapp/index.html', {'form': form, 'title': 'Enter Room'})

@login_required
def message_view(request, room_name):
    get_room = RoomModel.objects.get(room_name=room_name)
    get_messages = MessagesModel.objects.filter(room_name=get_room)

    if request.user not in get_room.members.all():
        get_room.members.add(request.user)
        messages.info(request, "You have been added to the chat.")

    context =  {
        'room': get_room,
        'room_name': room_name,
        'messages': get_messages,
        'user': request.user,
        'username': request.user.username,
        'current_date': timezone.now(),
        'yesterday': timezone.now() - timedelta(1),
    }

    return render(request, 'chatapp/message.html', context)


class MainPageView(ListView):
    template_name = 'chatapp/mainpage.html'
    context_object_name = 'chats'
    paginate_by = 8
    extra_context = {'title': 'Chats'}

    def get_queryset(self):
        chat_list = RoomModel.objects.filter(is_closed=False).annotate(num_members=models.Count('members')).order_by('-num_members')
        return chat_list