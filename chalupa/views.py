from django.http import request, HttpResponseRedirect
from datetime import datetime, date, timedelta
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views import generic
from django.views.generic import ListView, FormView, View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Room, Booking
from .forms import AvailabilityForm, Calendar, BookingForm
import calendar
from chalupa.booking_functions.availability import availability


# Create your views here.


# domovská stránka
def index(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)


# seznam pokojů
'''def RoomListView(request):
room = Room.objects.all()[0]
    room_Names = dict(room.room_names)
    room_values = room_Names.values()
    room_list = []
    for room_name in room_Names:
        room = room_Names.get(room_name)
        room_url = reverse('chalupa:RoomDetailView', kwargs={'name': room_name})
        room_list.append((room, room_url))
    context = {
        "room_list": room_list,
    }
    return render(request, 'room_list_view.html', context)'''


class RoomListView(generic.ListView):
    model = Room
    context_object_name = 'room_list'
    template_name = 'chalupa/room_list.html'


# seznam rezervací (pro admina)
class BookingList(LoginRequiredMixin, ListView):
    model = Booking

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list


# detail pokoje
'''class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        name = self.kwargs.get('name', None)
        form = AvailabilityForm()
        room_list = Room.objects.filter(name=name)

        if len(room_list) > 0:
            room = room_list[0]
            room_name = dict(room.room_names).get(room.name, None)
            context = {
                'room_name': room_name,
                'form': form
            }
            return render(request, 'room_detail_view.html', context)
        else:
            return HttpResponse('Tento pokoj neexistuje')'''


class RoomDetailView(generic.DetailView):
    model = Room
    context_object_name = 'room_detail'
    template_name = 'chalupa/room_detail.html'


# Toto je nadbytečné
    def post(self, request, *args, **kwargs):
        name = self.kwargs.get('name', None)
        room_list = Room.objects.filter(name=name)
        form = AvailabilityForm(request.POST)
        if availability(data['check_in'], data['check_out']):
            bookings = Booking.objects.create(
                user=self.request.user,
                check_in=data['check_in'],
                check_out=data['check_out'],
            )
            bookings.save()
            return HttpResponse(bookings)
        else:
            return HttpResponse('Tenhle termín je už rezervovaný')
        form.print_form()
        return super().form_valid(form)


# rezervace termínu
class BookingView(LoginRequiredMixin, FormView):
    form_class = AvailabilityForm
    template_name = 'availability_form.html'

    def form_valid(self, form):
        data = form.cleaned_data
        if availability(data['check_in'], data['check_out']):
            bookings = Booking.objects.create(
                user=self.request.user,
                check_in=data['check_in'],
                check_out=data['check_out'],
                number_of_guests=data['number_of_guests'],
                #note=data['note'],
            )
            bookings.save()
            return HttpResponse(bookings)
        else:
            return HttpResponse('Tento termín už je rezervovaný')
        form.print_form()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)

        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def booking(request, booking_id=None):
    instance = Booking()
    if booking_id:
        instance = get_object_or_404(Booking, pk=booking_id)
    else:
        instance = Booking()

    form = BookingForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('chalupa:BookingView'))
    return render(request, 'chalupa/booking_form.html', {'form': form})


def gallery(request):
    return render(request, 'chalupa/gallery.html')


def view_image(request, pk):
    return render(request, 'chalupa/gallery.html')


def add_image(request):
    return render(request, 'chalupa/image_add.html')


'''class CalendarView(generic.ListView):
    model = Booking
    template_name = 'availability_form.html'
    '''







