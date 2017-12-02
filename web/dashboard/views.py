from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ParcelForm, RoomForm, SearchForm
from .models import Parcel, Room
from .emails import new_parcel_notification

# Views
def index(request, template_name='index.html'):
    info = {'action':'Search'}
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if (form.is_valid()):
            # go to room page
            return redirect('room', number=request.POST['room_number'])
    else:
        form = SearchForm()
    return render(request, template_name, {'form':form, 'info':info})

def room(request, number, template_name='list.html'):
    parcels = []
    room_query = Room.objects.filter(number=number)
    print(room_query)
    if (room_query):
        room = room_query[0]
        parcels = Parcel.objects.filter(room=room)
    return render(request, template_name, {'object_list':parcels, 'number':number})

# Admin Views
def index(request, template_name='index.html'):
    info = {'action':'Search'}
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if (form.is_valid()):
            # go to room page
            return redirect('room', number=request.POST['room_number'])
    else:
        form = SearchForm()
    return render(request, template_name, {'form':form, 'info':info})
