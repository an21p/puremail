import datetime

from django import forms
from .models import Room, Parcel, Resident
from django.core.validators import MaxValueValidator, MinValueValidator

class EmptyForm(forms.Form):
    pass

class EmailForm(forms.Form):
    email = forms.EmailField()

class ParcelForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ('room', 'quantity', 'sender')
        exclude = ('date_delivered', 'date_received')
