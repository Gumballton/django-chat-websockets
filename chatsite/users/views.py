from typing import Any, Dict
from django import forms
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
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

    """
    View for user login.

    Inherits from Django's LoginView.

    Attributes:
        form_class: Form class for user login.
        template_name: Template for rendering login page.
        extra_context: Extra context data for rendering template.
        success_url: URL to redirect to after successful login.
    """

    form_class = UserLoginForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Login'}
    success_url = reverse_lazy('chatapp:create-room')


class RegisterUser(CreateView):

    """
    View for user registration.

    Inherits from Django's CreateView

    Attributes:
        form_class: Form class for user registration.
        template_name: Template for rendering registration page.
        extra_context: Extra context data for rendering template.
        success_url: URL to redirect to after successful registration.
    """

    form_class = RegisterUserForm
    template_name = 'users/register_or_login.html'
    extra_context = {'title': 'Registration'}
    success_url = reverse_lazy('users:login')


def logout_user(request: HttpRequest) -> HttpResponseRedirect:
    """
    View for user logout.

    Logs out the user and redirects to login page.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponseRedirect: Redirects to login page.
    """
    logout(request)
    return redirect('users:login')

def leave_chat(request: HttpRequest, room_id: int) -> HttpResponseRedirect:
    """
    View for leaving a chat room.

    Removes the user from the specified chat room and redirects to main page.

    Args:
        request: HttpRequest object.
        room_id: ID of the chat room.

    Returns:
        HttpResponseRedirect: Redirects to main page.
    """
    room = get_object_or_404(RoomModel, id=room_id)

    if request.user in room.members.all():
        room.members.remove(request.user)

    return redirect('chatapp:mainpage')

class UserProfileView(ListView):

    """
    View for profile.

    Inherits from Django's ListView

    Attributes:
        model: Model for the user.
        template_name: Template for rendering user profile page.
        context_object_name: Name of the variable to use in the template for the list of objects.
        extra_context: Extra context data for rendering template.
        paginate_by: Number of objects to display per page.
    """

    model = get_user_model()
    template_name = 'chatapp/mainpage.html'
    context_object_name = 'chats'
    extra_context = {'title': 'User Profile'}
    paginate_by = 8

    def get_queryset(self) -> QuerySet:
        """
        Get queryset for user profile.

        Returns:
            QuerySet: QuerySet of chat rooms where the user is either owner or member.
        """
        user = self.request.user
        queryset = RoomModel.objects.filter(owner=user) | RoomModel.objects.filter(members=user)
        return queryset.distinct()
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        Get extra context data.

        Adds the current user to the context.

        Args:
            kwargs: Keyword arguments.

        Returns:
            dict: Extra context data.
        """
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class AddMemberView(LoginRequiredMixin, FormView):

    """
    View for adding a member to a chat room.

    Inherits from Django's LoginRequiredMixin and FormView.

    Attributes:
        form_class: Form class for adding a member.
        template_name: Template for rendering the form.
    """

    form_class = AddMemberFrom
    template_name = 'users/register_or_login.html'


    def form_valid(self, form: forms.Form) -> HttpResponseRedirect:
        """
        Handle form submission.

        Adds the specified user to the chat room if the current user is the owner.

        Args:
            form: Form instance.

        Returns:
            HttpResponseRedirect: Redirect to room page. 
        """
        room_name = self.kwargs['room_name']
        room = RoomModel.objects.get(room_name=room_name)
        
        if room.owner == self.request.user:
            user = form.cleaned_data['user']
            room.members.add(user)
            messages.success(self.request, f'{user.username} added to the chat successfully.')
        else:
            messages.error(self.request, 'Only the owner can add members to the chat.')
        
        return redirect('chatapp:room', room_name=room_name)

    def get_success_url(self) -> forms.Form:
        """
        Get success URL.

        Returns:
            HttpResponseRedirect: Redirect to main page.
        """
        return redirect('chatapp:mainpage')
    




class ChangeUserPassword(PasswordChangeView):

    """
    View for changing user's password.

    Inherits from Django's PasswordChangeView.

    Attributes:
        form_class: Form class for changing password.
        template_name: Template for rendering the form.
        success_url: URL to redirect to after successful password change.
    """

    form_class = ChangePasswordForm
    template_name = 'users/register_or_login.html'
    success_url = reverse_lazy('users:change_user_password_done')
    