from django.http import request
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView, View
from .models import Room, Booking
from .forms import AvailabilityForm
from chalupa.booking_functions.availability import availability

# Create your views here.


# domovská stránka
def index(request):
    return render(request, 'index.html')


# seznam pokojů
class RoomListView(ListView):
    model = Room


# seznam rezervací (pro admina)
class BookingList(ListView):
    model = Booking


# detail pokoje
class RoomDetailView(View):
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
            return HttpResponse('Tento pokoj neexistuje')

    def post(self, request, *args, **kwargs):
        name = self.kwargs.get('name', None)
        room_list = Room.objects.filter(name=name)
        form = AvailabilityForm(request.POST)
        if availability(data['check_in'], data['check_out']):
            bookings = Booking.objects.create(
                user = self.request.user,
                check_in = data['check_in'],
                check_out = data['check_out'],
            )
            bookings.save()
            return HttpResponse(bookings)
        else:
            return HttpResponse('Tenhle termín je už rezervovaný')
        form.print_form()
        return super().form_valid(form)


# rezervace termínu
class BookingView(FormView):
    form_class = AvailabilityForm
    template_name = 'availability_form.html'

    def form_valid(self, form):
        data = form.cleaned_data
        if availability(data['check_in'], data['check_out']):
            bookings = Booking.objects.create(
                user = self.request.user,
                check_in = data['check_in'],
                check_out = data['check_out'],
            )
            bookings.save()
            return HttpResponse(bookings)
        else:
            return HttpResponse('Tento termín už je rezervovaný')
        form.print_form()
        return super().form_valid(form)