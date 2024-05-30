from django import forms

from .models import RoomModel

class RoomCreateForm(forms.ModelForm):

    """
    Form class for creating a chat room.

    This form is used to create a new chat room. It includes fields
    for the room name, description, and whether it is private or not.  
    """

    class Meta:
        model = RoomModel
        fields = ['room_name', 'description', 'is_closed']
        labels = {'is_closed': 'Private chat'}
        widgets = {
            'room_name': forms.TextInput(attrs={'class': 'form-control', 'style': "margin: 0; padding: 7px; border: 1px solid #ccc; font-size: 16px;"}),
            'description': forms.Textarea(attrs={'class': 'form-control','cols': 60, 'rows': 1}),
            'is_closed': forms.CheckboxInput(attrs={'class':'form-check-input mt-0'})
        }

    def clean_room_name(self) -> str:

        """
        Custom validation method for the room name.

        Ensures that the room name is unique.
        """

        name = self.cleaned_data['room_name']
        if RoomModel.objects.filter(room_name=name).exists():
            raise forms.ValidationError('This chat already exist')
        return name


class RoomEnterForm(forms.ModelForm):

    """
    Form class for entering a chat room.

    This form is used to enter an existing chat room. It includes
    a field for the room name.
    """

    class Meta:
        model = RoomModel
        fields = ['room_name']

    def clean_room_name(self) -> str:

        """
        Custom validation method for the room name.

        Ensures that the room name corresponds to an existing chat room.
        """

        name = self.cleaned_data['room_name']
        if not RoomModel.objects.filter(room_name=name).exists():
            raise forms.ValidationError('This chat does not exist')
        return name