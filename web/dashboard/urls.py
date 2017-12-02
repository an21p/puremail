from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^parcel/$', views.all_parcels, name='all_parcels'),
    url(r'^parcel/add/$', views.parcel_add, name='parcel_add'),
    url(r'^parcel/update/(?P<pk>\d+)$', views.parcel_update, name='parcel_update'),
    url(r'^parcel/delete/(?P<pk>\d+)$', views.parcel_delete, name='parcel_delete'),
    url(r'^room/(?P<number>\d+)$', views.room, name='room'),
]
