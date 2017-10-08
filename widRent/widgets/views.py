from django.shortcuts import render, redirect, get_object_or_404
from .models import Widget
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status


def index(request):
    instance = Widget.objects.all()
    context = {
        'instance': instance,
    }
    return render(request, 'widgets/index.html', context)


def page(request, pk):
    obj = get_object_or_404(Widget,pk=pk)

    context = {
        'obj': obj,
    }
    return render(request, 'widgets/page.html', context)

def contacts(request):
    return render(request, 'contacts.html')

# --------------- api -----------------------

class Unmark(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None, format=None):

        obj = get_object_or_404(Widget, pk=pk)
        user = self.request.user
        liked, disliked = obj.unmark(user)
        if liked != None:
            data = {
                'liked': liked,
                'disliked': disliked,
            }
            return Response(data)
        return Response(-1)



class Likes(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None, format=None):

        obj = get_object_or_404(Widget, pk=pk)
        user = self.request.user
        liked, disliked = obj.like(user)
        if liked != None:
            data = {
                'liked': liked,
                'disliked': disliked,
            }
            return Response(data)
        return Response(-1)


class Dislikes(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None, format=None):

        obj = get_object_or_404(Widget, pk=pk)
        user = self.request.user
        liked, disliked = obj.dislike(user)
        if liked != None:
            data = {
                'liked': liked,
                'disliked': disliked,
            }
            return Response(data)
        return Response(-1)

