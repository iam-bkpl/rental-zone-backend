
from django import forms
from rooms.models import Room, Review,RATE_CHOICES

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        
        

class RateForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(),required=False)
    rate = forms.ChoiceField(choices=RATE_CHOICES,widget=forms.Select(), required=True)
    
    
    
    class Meta:
        model = Review
        fields = ('text','rate')