import codecs
from datetime import timedelta

from django.core.mail import send_mail, EmailMessage
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
    html_content = '<p>You have received a new <a href="'+link+'">parcel</a>.</p><p>To unsubscribe use this <a href="'+ unsubscribe +'">link</a></p>'
    from_addr = 'from@ubreal.co.uk'
    to_addr = [str(resident.email)]
    msg = EmailMessage(subject, html_content, from_addr, to_addr)
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()

def subscription_notification(resident):
    unsubscribe = url+'/unsubscribe/'+encode(resident.id)
    subject = 'Room '+str(resident.room.number)+' subscription'
    html_content = '<p>To unsubscribe use this <a href="'+unsubscribe+'">link</a></p>'
    from_addr = 'from@ubreal.co.uk'
    to_addr = [str(resident.email)]
    msg = EmailMessage(subject, html_content, from_addr, to_addr)
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
