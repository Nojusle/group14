from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from widgets.models import Widget, Rent, Basket
from .utils import calc_angle
from matching_settings import dislike_item, liked_item, not_rated_item, recommend_people_count

from django.db.models import Prefetch, Count

from django.db.models import Count, F, Q, Case, When, Prefetch, Value, CharField

def user(request):
    user = request.user
    if user.is_authenticated():

        user_vector = Widget.objects.get_vector_for_user(user)
        print('\n\n\n\n\n')
        print('%s - liked item'%liked_item)
        print('%s - disliked item'%dislike_item)
        print('%s - not rated item'%not_rated_item)

        print('\n\n\n\n\n')

        print(user.username + ' vector is ', user_vector)
        print('\n')

        # gets all users except current user and adds to dictionary
        angles_dict = {}

        for other_user in User.objects.exclude(id=user.id):
            vector = Widget.objects.get_vector_for_user(other_user)
            angle = calc_angle(vector, user_vector)

            if angle < 90:
                angles_dict[other_user.pk] = angle

            print(other_user.username + ' vector is ', vector)
            print(user.username + ' - ' + other_user.username ,' : ', angle)
            print('\n')


        angles_dict = sorted(angles_dict.items(), key=lambda x: (-x[1], x[0]))

        user_count = recommend_people_count if len(angles_dict) > recommend_people_count else len(angles_dict)

        user_list = [angles_dict[x][0] for x in range(user_count)]

        recommendations = Widget.objects.filter(
                    liked__in=user_list).exclude(
                        liked=user).exclude(disliked=user).distinct()

        context = {
            'instance': recommendations,
        }
        return render(request, 'recommendations/user.html', context)

    return redirect('widgets:index')


def item(request):
    user = request.user
    if user.is_authenticated():

        liked_qs = user.likes.all()

        print('\n\nliked widgets:')
        for i in liked_qs:
            print(i.title)

        print('\ndisliked widgets:')
        for i in user.dislikes.all():
            print(i.title)

        print('\n\n')
        
        if request.method == 'POST':
            if 'update' in request.POST:
                Widget.objects.update_item_to_item_matching()

        recommended_list = {}
        tried = []
        for i in liked_qs:
            print('\n The liked item: ',i)
            angle_query = i.angles.prefetch_related(Prefetch('widgets', queryset=Widget.objects.exclude(
                                        disliked=user).exclude(liked=user))).distinct()
            for j in angle_query:
                if j.widgets.all():
                    print(' similar widgets: ', j.widgets.all())
                    obj = j.widgets.first()
                    if obj.pk not in tried:
                        tried.append(obj.pk)
                        recommended_list[j.angle] = obj



        # recommended_list = sorted(recommended_list.items(), key=lambda x: (-x[0], x[1]))
        # count_of_tiems = recommend_people_count if len(recommended_list) > recommend_people_count else len(recommended_list)
        # recommended_list = recommended_list[0:count_of_tiems]

        context = {
            'instance': recommended_list.items(),
        }

        return render(request, 'recommendations/item.html', context)

    return redirect('widgets:index')




def rented(request):
    user = request.user
    if user.is_authenticated():
        instance = Widget.objects.filter(rent__user=user, rent__active=True)
        history = Rent.objects.filter(user=user, active=False)



        # .annotate(user_rating=Case(
        #                                     When(widget__liked=user,then=Value('liked')),
        #                                     When(widget__disliked=user,then=Value('disliked')),
        #                                     default=Value('Not rated'),
        #                                     output_field=CharField()
        #                                     ))




# Client.objects.annotate(
# ...     discount=Case(
# ...         When(account_type=Client.GOLD, then=Value('5%')),
# ...         When(account_type=Client.PLATINUM, then=Value('10%')),
# ...         default=Value('0%'),
# ...         output_field=CharField(),
# ...     ),

        context = {
            'instance': instance,
            'history': history
        }

        return render(request, 'recommendations/rented.html', context)

    return redirect('widgets:index')



def basket(request):
    user = request.user
    if user.is_authenticated():
        try:
            instance = user.basket.widgets.all()
        except:
            basket = Basket(user=user)
            basket.save()
            instance = {}

        if request.method == 'POST':
            for obj in instance:
                obj.rent_it(user)
                user.basket.widgets.remove(obj)


            return redirect('recom:rented')

        context = {
            'instance': instance,
        }
        return render(request, 'recommendations/basket.html', context)










