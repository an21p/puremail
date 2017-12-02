from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import ParcelForm, RoomForm
from .models import Parcel, Room
from .emails import new_parcel_notification

# Views
def index(request, template_name='index.html'):
    info = {'action':'Search'}
    rooms = Room.objects.all()
    if request.method == 'POST':
        return redirect('room', number=request.POST['room_id'])
    return render(request, template_name, {'rooms':rooms, 'info':info})

def room(request, number, template_name='list.html'):
    info = {'name':'Room '+number}
    parcels = []
    room_query = Room.objects.filter(number=number)
    print(room_query)
    if (room_query):
        room = room_query[0]
        parcels = Parcel.objects.filter(room=room)
    return render(request, template_name, {'object_list':parcels, 'info':info})

# Admin Views
@login_required(login_url='/admin/login')
def all_parcels(request, template_name='list.html'):
    user = request.user
    if (not user.is_staff):
        return redirect('index')
    info = {'name':'All Parcels'}
    parcels = Parcel.objects.all()
    return render(request, template_name, {'object_list':parcels, 'info':info})

@login_required(login_url='/admin/login')
def parcel_add(request, template_name='form.html'):
    user = request.user
    if (not user.is_staff):
        return redirect('index')
    info = {'name':'Add New Parcel','action':'Add'}
    form = ParcelForm(request.POST or None)
    if request.method == 'POST':
        if (form.is_valid()):
            form.save()
            return redirect('all_parcels')
    return render(request, template_name, {'form':form, 'info':info})

@login_required(login_url='/admin/login')
def parcel_update(request, pk, template_name='form.html'):
    user = request.user
    if (not user.is_staff):
        return redirect('index')
    info = {'name':'Update Parcel','action':'Search'}
    parcel = get_object_or_404(Parcel, pk=pk)
    form = ParcelForm(request.POST or None, instance=parcel)
    if request.method == 'POST':
        if (form.is_valid()):
            form.save()
            return redirect('all_parcels')
    return render(request, template_name, {'form':form, 'info':info})

@login_required(login_url='/admin/login')
def parcel_delete(request, pk, template_name='form.html'):
    user = request.user
    if (not user.is_staff):
        return redirect('index')
    parcel = get_object_or_404(Parcel, pk=pk)
    parcel.delete()
    return redirect('all_parcels')
