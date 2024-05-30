from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

from chatapp.models import RoomModel


class UserLoginForm(AuthenticationForm):

    """
    Form for user login.

    Inherits from Django's AuthenticationForm.

    Attributes:
        model: Model for the user.
        fields: Fields to be displayed in the form.
    """

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class RegisterUserForm(UserCreationForm):

    """
    Form for user registration.

    Inherits from Django's UserCreationForm.

    Attributes:
        username: Field for user's login name.
        password1: Field for user's password.
        password2: Field for confirming the password.
        email: Field for user's email.
    """

    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email','password1', 'password2')
        labels = {'email': 'E-mail'}
        widgets = {'email': forms.TextInput(attrs={'class': 'form-input'})}


    def clean_email(self) -> str:

        """
        Clean email field and validate uniqueness.

        Returns:
            str: Cleaned email.
        """

        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('This E-mail already exists!')
        
        return email
    

class AddMemberFrom(forms.Form):

    """
    Form for adding a member to a chat room.

    Attributes:
        user: Field for entering the username of the user to be added.
    """

    user = forms.CharField(label='Username')

    def clean_user(self) -> get_user_model:
        """
        Clean user field and validate existence.

        Returns:
            User: User object.
        """
        username = self.cleaned_data['user']
        User = get_user_model()
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('User with this username does not exist.')
        
        return User.objects.get(username=username)
    

class ChangePasswordForm(PasswordChangeForm):

    """
    Form for changing user's password.

    Inherits from Django's PasswordChangeForm.

    Attributes:
        old_password: Field for entering the old password.
        new_password1: Field for entering the new password.
        new_password2: Field for confirming the new password.
    """

    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-input'}))