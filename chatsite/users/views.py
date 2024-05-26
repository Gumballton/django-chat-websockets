from django.db.models.query import QuerySet
from django.shortcuts import redirect, render

from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth import get_user_model


from chatapp.models import RoomModel
from users.forms import RegisterUserForm, UserLoginForm
# Create your views here.


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/register_or_login.html'
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


class UserProfileView(ListView):
    model = get_user_model()
    template_name = 'chatapp/mainpage.html'
    context_object_name = 'chats'
    extra_context = {'title': 'User Profile'}

    def get_queryset(self):
        user = self.request.user
        queryset = RoomModel.objects.filter(owner=user) | RoomModel.objects.filter(members=user)
        return queryset.distinct()
