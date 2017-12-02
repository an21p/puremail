import datetime

from django import forms
from .models import Room, Parcel, Resident
from django.core.validators import MaxValueValidator, MinValueValidator

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('number',)

class ResidentForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = ('email',)

class ParcelForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ('room', 'quantity', 'sender')
        exclude = ('date_delivered', 'date_received')
