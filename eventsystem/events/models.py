# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models



class Event(models.Model):
    RESTRICTION_CHOICES = (
        (1, "Volvox & Alkymisten, Delta, Naturviterne"),
        (2, "V&A, Delta, NV, HC, Nabla, Alle"),
    )
    title = models.CharField("title", max_length=50)
    start_date = models.DateTimeField("start date")
    end_date = models.DateTimeField("en date")
    location = models.CharField("location", max_length=50)
    description = models.TextField("description")
    seats = models.IntegerField("seats")
    restriction = models.SmallIntegerField("restriction", choices=RESTRICTION_CHOICES, default=2)
    
    @property
    def attendees(self):
        return map(lambda x: getattr(x, 'user'), AttendanceEntry.objects.filter(event=self))
    
    @models.permalink
    def get_absolute_url(self):
        return ('details', (), {'event_id': self.id})

    def get_restriction(self):
        return self.RESTRICTION_CHOICES[self.restriction-1][1]

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['start_date']

class AttendanceEntry(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __unicode__(self):
        return self.user.get_full_name()

    class Meta:
        unique_together = ("event", "user")
        ordering = ['timestamp']

