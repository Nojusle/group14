from django.conf.urls import url
from .views import user, item


app_name = 'recom'

urlpatterns = [
    url(r'^$', user, name='user'),
    url(r'^item/$', item, name='item'),
]



# urlpatterns = [
#     url(r'^$', index, name='index'),
#     url(r'^(?P<pk>[0-9]+)$', page, name='page'),
#     url(r'^(?P<pk>[0-9]+)/like$', Likes.as_view(), name='like'),
#     url(r'^(?P<pk>[0-9]+)/dislike$', Dislikes.as_view(), name='dislike'),

#     url(r'^contacts$', contacts, name='contacts'),
# ]
