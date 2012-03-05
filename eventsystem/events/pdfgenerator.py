# -*- coding: utf-8 -*-

from cStringIO import StringIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import styles, colors

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from eventsystem.events.models import Event

@login_required
def pdf(self, *args, **kwargs):
    event_id = kwargs['event_id']
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=påmeldte.pdf'

    event = get_object_or_404(EventWithAttendance, pk=event_id)
    attendees = sorted(event.attendees, key=lambda user: user.last_name)
    waiters = event.wait_list

    paragraph_style = styles.getSampleStyleSheet()['Normal']

    table_style = TableStyle(
            [('GRID', (0, 0), (-1, -1), 0.50, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('BACKGROUND', (0, 0), (4, 0), colors.lightgrey)
            ]
    )

    attendee_table_data = [('Nr', 'Navn', 'Klassetrinn', ' Studie', 'Telefon'), ]
    waiters_table_data = [('Nr', 'Navn', 'Klassetrinn', ' Studie', 'Telefon'), ]
    allergies_table_data = [('Nr', 'Navn', 'Matallergier'),]
    nr = 0


    for attendee in attendees:
        nr += 1
        attendee_table_data.append((nr, attendee.last_name + ", " + attendee.first_name ,
                            int(attendee.get_profile().year),
                            attendee.get_profile().get_field_of_study_display(),
                            attendee.get_profile().phone_number)
                            )
	if attendee.get_profile().allergies:
	    allergies_table_data.append((nr, attendee.last_name + ", " + attendee.first_name, attendee.get_profile().allergies))
    for waiter in waiters:
        nr += 1
        waiters_table_data.append((nr, waiter.last_name + ", " + waiter.first_name ,
                            int(waiter.get_profile().year),
                            waiter.get_profile().get_field_of_study_display(),
                            waiter.get_profile().phone_number)
                            )
	if waiter.get_profile().allergies:
            allergies_table_data.append((nr, waiter.last_name + ", " + waiter.first_name, waiter.get_profile().allergies))

    waiter_row_heights = [16] * len(waiters_table_data)
    waiter_table = Table(waiters_table_data, (25, 250, 60, 40, 55), waiter_row_heights)
    waiter_table.setStyle(table_style)

    attendee_row_heights = [16] * len(attendee_table_data)
    attendee_table = Table(attendee_table_data, (25, 250, 60, 40, 55), attendee_row_heights)
    attendee_table.setStyle(table_style)

    allergies_row_heights = [16] * len(allergies_table_data)
    allergies_table = Table(allergies_table_data, (25, 200,300), allergies_row_heights)
    allergies_table.setStyle(table_style)

    tittel = paragraph_style
    tittel.alignment = 1

    components = []
    components.append(Paragraph("<b><font size='14'>" + event.title + "</font></b>", tittel))
    components.append(Spacer(700, 25))
    components.append(Paragraph("<b><font size='14'>" + "Påmeldte" + "</font></b>", tittel))
    components.append(Spacer(100,25))
    components.append(attendee_table)
    if waiters:
        components.append(Spacer(700, 25))
        components.append(Paragraph("<b><font size='10'>" + "Venteliste" + "</font></b>", tittel))
	components.append(Spacer(100,25))
        components.append(waiter_table)
    if len(allergies_table_data) > 1:	
    	components.append(Spacer(700, 25))
    	components.append(Paragraph("<b><font size='10'>" + "Matallergier" + "</font></b>", tittel))
	components.append(Spacer(100,25))
    	components.append(allergies_table)
	



    raw_pdf = StringIO()
    document = SimpleDocTemplate(raw_pdf)
    document.build(components)
    pdf = raw_pdf.getvalue()
    raw_pdf.close()
    response.write(pdf)

    return response
