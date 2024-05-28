from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from chatapp.models import RoomModel


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email','password1', 'password2')
        labels = {'email': 'E-mail'}
        widgets = {'email': forms.TextInput(attrs={'class': 'form-input'})}


    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('This E-mail already exists!')
        
        return email
    

class AddMemberFrom(forms.Form):
    user = forms.CharField(label='Username')

    def clean_user(self):
        username = self.cleaned_data['user']
        User = get_user_model()
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('User with this username does not exist.')
        
        return User.objects.get(username=username)
    