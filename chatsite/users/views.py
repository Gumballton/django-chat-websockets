from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib import messages

from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, ListView, FormView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import get_user_model


from chatapp.models import RoomModel
from users.forms import AddMemberFrom, ChangePasswordForm, RegisterUserForm, UserLoginForm
# Create your views here.


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Login'}
    success_url = reverse_lazy('chatapp:create-room')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register_or_login.html'
    extra_context = {'title': 'Registration'}
    success_url = reverse_lazy('users:login')


def logout_user(request):
    logout(request)
    return redirect('users:login')

def leave_chat(request, room_id):
    room = get_object_or_404(RoomModel, id=room_id)

    if request.user in room.members.all():
        room.members.remove(request.user)

    return redirect('chatapp:mainpage')

class UserProfileView(ListView):
    model = get_user_model()
    template_name = 'chatapp/mainpage.html'
    context_object_name = 'chats'
    extra_context = {'title': 'User Profile'}
    paginate_by = 8

    def get_queryset(self):
        user = self.request.user
        queryset = RoomModel.objects.filter(owner=user) | RoomModel.objects.filter(members=user)
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class AddMemberView(LoginRequiredMixin, FormView):
    form_class = AddMemberFrom
    template_name = 'users/register_or_login.html'


    def form_valid(self, form):
        room_name = self.kwargs['room_name']
        room = RoomModel.objects.get(room_name=room_name)
        
        if room.owner == self.request.user:
            user = form.cleaned_data['user']
            room.members.add(user)
            messages.success(self.request, f'{user.username} added to the chat successfully.')
        else:
            messages.error(self.request, 'Only the owner can add members to the chat.')
        
        return redirect('chatapp:room', room_name=room_name)

    def get_success_url(self):
        return redirect('chatapp:mainpage')
    




class ChangeUserPassword(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'users/register_or_login.html'
    success_url = reverse_lazy('users:change_user_password_done')
    