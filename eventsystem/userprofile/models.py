# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

from eventsystem.events.models import AttendanceEntry

FIELD_OF_STUDY_CHOICES = (
    (1, 'Volvox & Alkymisten'),
    (2, 'Delta'),
    (3, 'Naturviterne'),
    (4, 'HC'),
    (5, 'Nabla'),
    (6, 'Other'),
)

class UserProfile(models.Model):

    user = models.ForeignKey(User, unique=True)

    field_of_study = models.SmallIntegerField("linjeforening", choices=FIELD_OF_STUDY_CHOICES, default=6)
    study_program = models.CharField("studieretning", max_length=50, null=True, blank=True)
    year = models.IntegerField("klassetrinn", null=True, blank=True)

    def get_events(self):
        return map(lambda x: getattr(x, 'event'), AttendanceEntry.objects.filter(user=self.user))
    
    def get_number_of_events(self):
        return len(get_events())

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
