from dataclasses import field
from django import forms
from rooms.models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        
        