import numpy as np
from matching_settings import liked_item, dislike_item, not_rated_item

from datetime import datetime


from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from recommendations.models import Angle
from recommendations.utils import calc_angle



class WidgetManager(models.Manager):

    def get_vector_for_user(self, user):
        instance = super(WidgetManager, self).all()
        vector = []
        for widget in instance:
            if user in widget.liked.all():
                vector.append(liked_item)
            elif dislike_item != not_rated_item and user in widget.disliked.all():
                vector.append(dislike_item)
            else:
                vector.append(not_rated_item)
        return np.array(vector)


    def update_item_to_item_matching(self):
        all_widgets = super(WidgetManager, self).all()
        used_list = []
        print('\n\n\n\n\n')

        for widget in all_widgets:
            used_list.append(widget)
            widget_vector = widget.get_vector_for_widget()

            for widget2 in all_widgets:

                if widget2 not in used_list:
                    widget2_vector = widget2.get_vector_for_widget()
                    angle = calc_angle(widget_vector, widget2_vector)

                    if not angle < 90:
                        widget.delete_angle_obj(widget2)
                    else:
                        widget.add_item_angle(widget2, angle)


                        print(widget,'-',widget2)
                        print(widget_vector,'-', widget2_vector ,':',angle)



class Widget(models.Model):
    title     = models.CharField(max_length=250, db_index=True)

    quantity  = models.IntegerField(default=0)
    borrowed  = models.IntegerField(default=0)

    image     = models.ImageField(upload_to='widgets', null=True, blank=True)

    liked     = models.ManyToManyField(User, db_index=True, blank=True, related_name='likes')
    disliked  = models.ManyToManyField(User, db_index=True, blank=True, related_name='dislikes')
    catgory   = models.ManyToManyField('Category', blank=True)
    objects   = WidgetManager()

    def __str__(self):
        return self.title

    def get_like_url(self):
        return reverse('widgets:like', kwargs={'pk': self.pk})

    def get_dislike_url(self):
        return reverse('widgets:dislike', kwargs={'pk': self.pk})

    def get_unmark_url(self):
        return reverse('widgets:unmark', kwargs={'pk': self.pk})

    def get_abolute_url(self):
        return reverse('widgets:page', kwargs={'pk': self.pk})


    def get_angle_obj(self, widget):
        angle_qs = Angle.objects.filter(widgets=self)
        angle_obj = None
        try: 
            angle_obj = angle_qs.get(widgets=widget)
        except Angle.MultipleObjectsReturned:
            angle_qs.delete()
        except:
            pass
        return angle_obj


    def get_recommended_item(self, user):
        matching_items = self.angles.exclude(widgets__in=user.dislikes.all())
        return matching_items

    def delete_angle_obj(self, widget):
        angle_obj = self.get_angle_obj(widget)
        if angle_obj:
            angle_obj.delete()
        return angle_obj


    def add_item_angle(self, widget, angle):
        angle_obj = self.get_angle_obj(widget)
        if angle_obj:
            angle_obj.angle = angle
            angle_obj.save()
            print('----------- updated -----------')
        else:
            angle_obj = Angle(angle=angle)
            angle_obj.save()
            angle_obj.widgets.add(self)
            angle_obj.widgets.add(widget)
            print('----------- created -----------')

        print(self, '-', widget, ':', angle)
        return angle_obj




    def get_vector_for_widget(self):
        vector = []
        for user in User.objects.all():
            if user in self.liked.all():
                vector.append(liked_item)
            elif dislike_item != not_rated_item and user in self.disliked.all():
                vector.append(dislike_item)
            else:
                vector.append(not_rated_item)
        return np.array(vector)



    def unmark(self, user):
        if user.is_authenticated():
            liked = False
            disliked = False

            if user in self.liked.all():
                self.liked.remove(user)
                liked = True

            if user in self.disliked.all():
                self.disliked.remove(user)
                disliked = True

            return liked, disliked
        return None, None


    def like(self, user):
        if user.is_authenticated():
            liked = False
            disliked = False

            if user not in self.liked.all():
                self.liked.add(user)
                liked = True

            if user in self.disliked.all():
                self.disliked.remove(user)
                disliked = True

            return liked, disliked
        return None, None

    def dislike(self, user):
        if user.is_authenticated():
            liked = False
            disliked = False

            if user not in self.disliked.all():
                self.disliked.add(user)
                liked = True

            if user in self.liked.all():
                self.liked.remove(user)
                disliked = True

            return liked, disliked
        return None, None



    def rent_it(self, user):
        if self.quantity - self.borrowed > 0:
            new_rent = Rent(widget=self,
                            user=user)
            new_rent.save()
            self.borrowed += 1
            self.save()

    def return_it(self, user):
        if self.user_active_renter(user):

            rent_obj = self.rent_set.filter(user=user, active=True).first()

            rent_obj.active = False
            rent_obj.returned = datetime.now()
            rent_obj.save()

            self.borrowed += -1
            self.save()


    def add_to_basket(self, user):
        try:
            user.basket
        except:
            basket = Basket(user=user)
            basket.save()

        basket = user.basket
        basket.widgets.add(self)

        
    def user_active_renter(self, user):
        return self.rent_set.filter(user=user, active=True).exists()

    def user_unactive_renter(self, user):
        return self.rent_set.filter(user=user, active=False).exists()

class Category(models.Model):
    title     = models.CharField(max_length=250, db_index=True)





class Basket(models.Model):
    user   = models.OneToOneField(User, db_index=True, blank=True, null=True, related_name='basket')
    widgets     = models.ManyToManyField('Widget', db_index=True, blank=True)

    def __str__(self):
        return self.widget.title + ' - ' + self.user.username




class Rent(models.Model):
    active = models.BooleanField(default=True)

    widget = models.ForeignKey('Widget', null=True)
    user   = models.ForeignKey(User, db_index=True)

    rented   = models.DateTimeField(auto_now_add=True)
    returned = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return self.widget.title + ' - ' + self.user.username




