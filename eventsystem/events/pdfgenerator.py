# -*- coding: utf-8 -*-

from cStringIO import StringIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import styles, colors

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from eventsystem.events.models import Event

@login_required
def pdf(self, *args, **kwargs):
    event_id = kwargs['event_id']
    event = get_object_or_404(Event, pk=event_id)
    
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=attendees.pdf'

    attendees = sorted(event.attendees, key=lambda user: user.last_name)

    paragraph_style = styles.getSampleStyleSheet()['Normal']

    table_style = TableStyle(
            [('GRID', (0, 0), (-1, -1), 0.50, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('BACKGROUND', (0, 0), (4, 0), colors.lightgrey)
            ]
    )

    attendee_table_data = [('Nr', 'Navn', 'Student Union'), ]
    nr = 0


    for attendee in attendees:
        nr += 1
        attendee_table_data.append((
            nr, attendee.last_name + ", " + attendee.first_name ,
            attendee.get_profile().get_field_of_study()
    ))

    attendee_row_heights = [16] * len(attendee_table_data)
    attendee_table = Table(attendee_table_data, (25, 275, 130), attendee_row_heights)
    attendee_table.setStyle(table_style)

    tittel = paragraph_style
    tittel.alignment = 1

    components = []
    components.append(Paragraph("<b><font size='14'>" + event.title + "</font></b>", tittel))
    components.append(Spacer(700, 25))
    components.append(attendee_table)
	

    raw_pdf = StringIO()
    document = SimpleDocTemplate(raw_pdf)
    document.build(components)
    pdf = raw_pdf.getvalue()
    raw_pdf.close()
    response.write(pdf)

    return response
