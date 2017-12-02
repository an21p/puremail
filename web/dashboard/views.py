from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import ParcelForm, EmptyForm, EmailForm
from .models import Parcel, Room, Resident
from .emails import new_parcel_notification, subscription_notification, decode

from django.core.signals import request_finished
from django.dispatch import Signal, receiver

subscription = Signal(providing_args=["resident"])
new_parcel = Signal(providing_args=["resident"])

@receiver(subscription)
def sub_callback(sender, **kwargs):
    subscription_notification(kwargs['resident'])

@receiver(new_parcel)
def parcel_call(sender, **kwargs):
    new_parcel_notification(kwargs['resident'])

# Views
def index(request, template_name='index.html'):
    if ('resident_email' not in request.session):
        return redirect('resident_login')
    info = {'action':'Search'}
    rooms = Room.objects.all()
    if request.method == 'POST':
        return redirect('room', pk=request.POST['room_id'])
    return render(request, template_name, {'rooms':rooms, 'info':info})

def resident_login(request, template_name='form.html'):
    if ('resident_email' in request.session):
        return redirect('index')
    info = {'name':'Resident Login','action':'Next'}
    form = EmailForm(request.POST or None)
    if request.method == 'POST':
        if (form.is_valid()):
            resident_email = request.POST['email']
            request.session['resident_email'] = resident_email
            if (not Resident.objects.filter(email=resident_email).exists()):
                return redirect('index')
            else:
                # if resident exists redirect to room
                resident = Resident.objects.filter(email=resident_email)[0]
                request.session['room'] = resident.room.number
                return redirect('room', resident.room.id)
    return render(request, template_name, {'info':info, 'form':form})

def room(request, pk, template_name='list.html'):
    if ('resident_email' not in request.session):
        return redirect('resident_login')
    resident_email = request.session['resident_email']
    parcels = []
    room = get_object_or_404(Room, pk=pk)
    info = {
    'name':'Room '+str(room.number),
    'action':'Subscribe',
    }
    form = EmptyForm(request.POST or None)
    if request.method == 'POST':
        # save resident
        if (not Resident.objects.filter(email=resident_email).exists()):
            resident = Resident(email=resident_email, room=room)
            resident.save()
            request.session['room'] = room.number
            subscription.send(sender='room', resident=resident)
        else:
            resident = Resident.objects.filter(email=resident_email)[0]
            request.session['room'] = resident.room.number
            info['error'] = 'Already Subscribed to a Room'
    if ('room' in request.session):
        info['room'] = request.session['room']
    parcels = reversed(Parcel.objects.filter(room=room))
    return render(request, template_name, {'object_list':parcels, 'info':info, 'room':room, 'form':form})

def room_hide(request, pk, template_name='list.html'):
    if ('resident_email' not in request.session):
        return redirect('resident_login')
    resident_email = request.session['resident_email']
    parcels = []
    room = get_object_or_404(Room, pk=pk)
    info = {
    'name':'Room '+str(room.number),
    'action':'Subscribe',
    }
    form = EmptyForm(request.POST or None)
    if request.method == 'POST':
        # save resident
        if (not Resident.objects.filter(email=resident_email).exists()):
            resident = Resident(email=resident_email, room=room)
            resident.save()
            request.session['room'] = room.number
            subscription.send(sender='room_hide', resident=resident)
        else:
            resident = Resident.objects.filter(email=resident_email)[0]
            request.session['room'] = resident.room.number
            info['error'] = 'Already Subscribed to a Room'
    if ('room' in request.session):
        info['room'] = request.session['room']
    parcels = reversed(Parcel.objects.filter(room=room).exclude(date_received__isnull=False))
    return render(request, template_name, {'object_list':parcels, 'info':info, 'room':room, 'form':form})

def unsubscribe(request, pk, template_name='unsubscribed.html'):
    dpk = decode(pk)
    try:
        resident = Resident.objects.get(pk=dpk)
        resident.delete()
        if ('resident_email' in request.session):
            del request.session['resident_email']
        if ('room' in request.session):
            del request.session['room']
    except Resident.DoesNotExist:
        print('Not Found')
    return render(request, template_name)

# Admin Views
@login_required(login_url='/admin/login')
def all_parcels(request, template_name='list.html'):
    user = request.user
    if (not user.is_staff):
        return redirect('index')
    info = {'name':'All Parcels'}
    parcels = reversed(Parcel.objects.all())
    return render(request, template_name, {'object_list':parcels, 'info':info})

@login_required(login_url='/admin/login')
def all_parcels_hide(request, template_name='list.html'):
    user = request.user
    if (not user.is_staff):
        return redirect('index')
    info = {'name':'All Parcels'}
    parcels = reversed(Parcel.objects.exclude(date_received__isnull=False))
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
            room = get_object_or_404(Room, pk=request.POST['room'])
            residents = Resident.objects.filter(room=room)
            for resident in residents:
                new_parcel.send(sender='parcel_add', resident=resident)
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
def parcel_delete(request, pk):
    user = request.user
    if (not user.is_staff):
        return redirect('index')
    parcel = get_object_or_404(Parcel, pk=pk)
    parcel.delete()
    return redirect('all_parcels')

@login_required(login_url='/admin/login')
def parcel_received(request, pk):
    user = request.user
    if (not user.is_staff):
        return redirect('index')
    parcel = get_object_or_404(Parcel, pk=pk)
    parcel.date_received = datetime.now()
    parcel.save()
    return redirect('all_parcels')
