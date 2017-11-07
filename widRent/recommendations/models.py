from django.db import models


class Angle(models.Model):
    angle   = models.FloatField(max_length=250, db_index=True)
    widgets = models.ManyToManyField('widgets.Widget', db_index=True, related_name='angles')

# class Angle2(models.Model):
#     angle   = models.FloatField(max_length=250, db_index=True)
#     widgets = models.ForeignKey('widgets.Widget', null=True, related_name='movieA')
#     widgets = models.ForeignKey('widgets.Widget', null=True, related_name='movieB')

