from django.shortcuts import render, redirect, get_object_or_404
from .models import Widget
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status

from django.db.models import F





def index(request):

    instance = Widget.objects.annotate(available=F('quantity')-F('borrowed'))
    context = {
        'instance': instance,
    }
    return render(request, 'widgets/index.html', context)


def page(request, pk):
    obj = get_object_or_404(Widget,pk=pk)
    if obj:
        user = request.user
        if user.is_authenticated():
            if request.method == 'POST':
                print('postlkmlk')
                rentred = request.POST.get('RENT')
                if rentred:
                    obj.add_to_basket(user)
                    print('rented')

                returned = request.POST.get('RETURN')
                if returned:
                    obj.return_it(user)
                    print('returned')

            obj.user_is_renting = obj.user_active_renter(user)
            obj.user_has_rented = obj.user_unactive_renter(user)


            obj.available = obj.quantity - obj.borrowed

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

