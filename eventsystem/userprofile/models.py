# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

from eventsystem.events.models import AttendanceEntry

FIELD_OF_STUDY_CHOICES = (
    (0, 'ANNEN'),
    (1, 'VOLVOX & ALK'),
    (2, 'NABLA'),
    (3, 'DELTA'),
)

class UserProfile(models.Model):

    user = models.ForeignKey(User, unique=True)

    field_of_study = models.SmallIntegerField("linjeforening", choices=FIELD_OF_STUDY_CHOICES, default=0)
    study_program = models.CharField("studieretning", max_length=50, null=True, blank=True)
    year = models.IntegerField("klassetrinn", null=True, blank=True)

    verify_token = models.CharField(max_length=32, editable=False, default='')

    def get_events(self):
        return map(lambda x: getattr(x, 'event'), AttendanceEntry.objects.filter(user=user))
    
    def get_number_of_events(self):
        return len(get_events())

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
