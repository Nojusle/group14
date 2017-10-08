from django.conf.urls import url
from .views import Likes, Dislikes, index, page, contacts, Unmark
app_name = 'widgets'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<pk>[0-9]+)$', page, name='page'),
    url(r'^(?P<pk>[0-9]+)/like$', Likes.as_view(), name='like'),
    url(r'^(?P<pk>[0-9]+)/dislike$', Dislikes.as_view(), name='dislike'),
    url(r'^(?P<pk>[0-9]+)/unmark$', Unmark.as_view(), name='unmark'),

    url(r'^contacts$', contacts, name='contacts'),
]
