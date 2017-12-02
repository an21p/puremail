import datetime

from django.db import models
from pgcrypto import EncryptedEmailField
from django.core.validators import MaxValueValidator, MinValueValidator

class Room(models.Model):
    number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(700)])
    email = EncryptedEmailField(
        verbose_name='Email address')
    subscribed = models.BooleanField(default=False)

class Parcel(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)])
    sender = models.CharField(max_length=40, null=True, blank=True)
    date_delivered = models.DateField(auto_now_add=True)
    date_received = models.DateField(null=True)
