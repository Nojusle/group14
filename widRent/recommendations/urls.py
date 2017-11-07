from django.conf.urls import url
from .views import user, item, rented, basket


app_name = 'recom'

urlpatterns = [
    url(r'^$', user, name='user'),
    url(r'^item/$', item, name='item'),
    url(r'^rented/$', rented, name='rented'),
    url(r'^basket/$', basket, name='basket'),
]


