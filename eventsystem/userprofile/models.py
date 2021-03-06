# -*- coding: utf-8 -*-

from datetime import datetime

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

    field_of_study = models.SmallIntegerField("student union", choices=FIELD_OF_STUDY_CHOICES, default=6)
    study_program = models.CharField("field of study", max_length=50, null=True, blank=True)
    year = models.IntegerField("year", null=True, blank=True)

    def get_events(self):
        return map(lambda x: getattr(x, 'event'), AttendanceEntry.objects.filter(user=self.user, event__start_date__gte=datetime.now()))
   
    def get_all_events(self):
        return map(lambda x: getattr(x, 'event'), AttendanceEntry.objects.filter(user=self.user))

    def get_number_of_events(self):
        return len(get_events())
    
    def get_field_of_study(self):
        return FIELD_OF_STUDY_CHOICES[self.field_of_study - 1][1]

    def is_attending_dinner(self):
        events = self.get_all_events()

        for event in events:
            if event.title == 'Middag':
                return True

    def can_attend_dinner(self):
        if self.is_attending_dinner():
            return False
        else:
            return len(self.get_events()) >= 2

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
