from django.shortcuts import redirect, render

from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import logout

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