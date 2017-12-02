import codecs
from datetime import timedelta

from django.core.mail import send_mail
from django.conf import settings
from cryptography.fernet import Fernet

f = Fernet(str.encode(settings.FERNET_KEY))

url = 'http://'+settings.APP_URL

def encode(pk):
    return codecs.encode(f.encrypt(str.encode(str(pk))),"hex").decode()

def decode(pk):
    return int(f.decrypt(codecs.decode(str.encode(pk),"hex")))

def new_parcel_notification(resident):
    link = url+'/room/'+str(resident.room.number)
    unsubscribe = url+'/unsubscribe/'+encode(resident.id)
    subject = 'New Parcel Room '+str(resident.room.number)
    message = 'You have received a new parcel '+link+'\nTo unsubscribe use this link '+unsubscribe
    from_addr = 'from@ubreal.co.uk'
    to_addr = [str(resident.email)]
    send_mail(subject, message, from_addr, to_addr, fail_silently=False)

def subscription_notification(resident):
    unsubscribe = url+'/unsubscribe/'+encode(resident.id)
    subject = 'Room '+str(resident.room.number)+' subscription'
    message = 'To unsubscribe use this link '+unsubscribe
    from_addr = 'from@ubreal.co.uk'
    to_addr = [str(resident.email)]
    send_mail(subject, message, from_addr, to_addr, fail_silently=False)
