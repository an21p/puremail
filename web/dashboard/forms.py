import datetime

from django import forms
from .models import Room, Parcel
from django.core.validators import MaxValueValidator, MinValueValidator

class SearchForm(forms.Form):
    room_number = forms.ChoiceField(choices=[(x, x) for x in range(1, 700)])

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('number', 'email')
        exclude = ('subscribed',)

class ParcelForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ('room', 'quantity', 'sender')
        exclude = ('date_delivered', 'date_received')
