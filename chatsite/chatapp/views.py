from datetime import timedelta

from django.db.models.query import QuerySet
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib import messages
from django.db import models
from django.http import HttpRequest, HttpResponse

from chatapp.models import MessagesModel, RoomModel
from .forms import RoomCreateForm, RoomEnterForm

# Create your views here.

@login_required
def create_room(request: HttpRequest) -> HttpResponse:

    """
    View to create a new chat room.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Redirects to the created room or renders the creation form.
    """

    if request.method == 'POST':
        form = RoomCreateForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.owner = request.user
            room.save()
            room.members.add(request.user)
            return redirect('chatapp:room', room_name=room.room_name)
    else:
        form = RoomCreateForm()

    return render(request, 'chatapp/index.html', {'form': form, 'title': 'Create Room'})

@login_required
def enter_room(request: HttpRequest) -> HttpResponse:

    """
    View to enter an existing chat room.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Redirects to the entered room or renders the entering form.
    """

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
def delete_chat(request: HttpRequest, room_id: int) -> HttpResponse:

    """
    View to delete a chat room.

    Args:
        request: HttpRequest object.
        room_id: ID of the room to be deleted.

    Returns:
        HttpResponse: Redirects to the main page after deleting the chat room.
    """

    room = get_object_or_404(RoomModel, pk=room_id)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Chat deleted successfully.')
        return redirect('chatapp:mainpage')
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def message_view(request: HttpRequest, room_name: str) -> HttpResponse:

    """
    View to display messages in a chat room.

    Args:
        request: HttpRequest object.
        room_name: Name of the chat room.

    Returns:
        HttpResponse: Renders the message view template.
    """

    get_room = RoomModel.objects.get(room_name=room_name)
    get_messages = MessagesModel.objects.filter(room_name=get_room)

    if get_room.is_closed:
        if request.user not in get_room.members.all() and request.user != get_room.owner:
            messages.info(request, "You need an invitation to join this chat.")
            return redirect('chatapp:mainpage')
    else:
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

    """
    View to display the main page with chat rooms.

    Attributes:
        template_name (str): Template name for rendering the main page.
        context_object_name (str): Name of the variable to be used in the template for the chat rooms.
        paginate_by (int): Number of chat rooms to display per page.
        extra_context (dict): Extra context data to pass to the template.

    Methods:
        get_queryset(self): Retrieve the list of open chat rooms sorted by the number of members.
    """

    template_name = 'chatapp/mainpage.html'
    context_object_name = 'chats'
    paginate_by = 8
    extra_context = {'title': 'Chats'}

    def get_queryset(self) -> models.QuerySet:
        chat_list = RoomModel.objects.filter(is_closed=False).annotate(num_members=models.Count('members')).order_by('-num_members')
        return chat_list