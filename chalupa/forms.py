from django import forms
from datetime import datetime, timedelta, date
from django.forms import ModelForm, DateInput
from calendar import HTMLCalendar
from .models import Booking


class AvailabilityForm(forms.Form):
    check_in = forms.DateField(required=True, input_formats=['%Y-%m-%d', ])
    check_out = forms.DateField(required=True, input_formats=['%Y-%m-%d', ])
    number_of_guests = forms.IntegerField(required=True)
    note = forms.CharField(required=False, widget=forms.Textarea)
    def print_form(self):
        pass


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        widgets = {
            'check_in': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%d'),
            'check_out': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = ('check_in', 'check_out', 'number_of_guests', 'note')

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['check_in'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['check_out'].input_formats = ('%Y-%m-%dT%H:%M',)


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter bookings by day
    def formatday(self, day, bookings):
        bookings_per_day = bookings.filter(check_in__day=day)
        d = ''
        for booking in bookings_per_day:
            d += f'<li class="list-group-item"> {booking.get_html_url} </li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
            # if date.today() == date(self.year, self.month, day):
            # return f"<td class='today'><div class='d-flex justify-content-between'><span class='date'>{day}</span>{Booking.get_date(self, self.year, self.month, day)}</div><ul> {d} </ul></td>"
            # return f"<td><div class='d-flex justify-content-between'><span class='date'>{day}</span>{Booking.get_date(self, self.year, self.month, day)}</div><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, week, bookings):
        w = ''
        for d, weekday in week:
            w += self.formatday(d, bookings)
        return f'<tr> {w} </tr>'

    # formats a month as a table
    # filter bookings by year and month
    def formatmonth(self, withyear=True):
        bookings = Booking.objects.filter(check_in__year=self.year, check_in__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, bookings)}\n'
        return cal
