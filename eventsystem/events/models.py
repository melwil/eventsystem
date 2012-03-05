# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models



class Event(models.Model):
    RESTRICTION_CHOICES = (
        (1, "Volvox & Alk, Delta, Naturviterne"),
        (2, "V&A, Delta, NV, HC, Nabla"),
        (3, "Alle"),
    )
    title = models.CharField("tittel", max_length=50)
    start_date = models.DateTimeField("startdato")
    end_date = models.DateTimeField("sluttdato")
    location = models.CharField("sted", max_length=50)
    description = models.TextField("beskrivelse")
    seats = models.IntegerField("plasser")
    restriction = models.SmallIntegerField("begrensning", choices=RESTRICTION_CHOICES, default=3)
    

    @property
    def attendees(self):
        return map(lambda x: getattr(x, 'user'), AttendanceEntry.objects.filter(event=self))
    
    @models.permalink
    def get_absolute_url(self):
        return ('details', (), {'event_id': self.id})

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['start_date']
        verbose_name = "arrangement"
        verbose_name_plural = "arrangementer"

class AttendanceEntry(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __unicode__(self):
        return self.user.get_full_name()

    class Meta:
        unique_together = ("event", "user")
        ordering = ['timestamp']

