from datetime import timedelta

from django.core.mail import send_mail
from django.core.signing import TimestampSigner, BadSignature
from django.conf import settings

url = 'http://'+settings.APP_URL

def new_parcel_notification(room):
    link = url+'/room/'+room.number
    subject = 'New Parcel'
    message = 'You have received a new parcel '+link
    from_addr = 'from@ubreal.co.uk'
    to_addr = [str(room.email)]
    send_mail(subject, message, from_addr, to_addr, fail_silently=False)
