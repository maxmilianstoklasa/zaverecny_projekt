from django.http import request, HttpResponseRedirect
from datetime import datetime, date, timedelta
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views import generic
from django.views.generic import ListView, FormView, View, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe

from .models import Room, Booking, Attachment, Category
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


class RoomListView(generic.ListView):
    model = Room
    context_object_name = 'room_list'
    template_name = 'chalupa/room_list.html'


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
    '''def post(self, request, *args, **kwargs):
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
        return super().form_valid(form)'''


# rezervace termínu
class BookingView(LoginRequiredMixin, FormView, ListView):
    form_class = AvailabilityForm
    template_name = 'chalupa/booking_view.html'

    def form_valid(self, form):
        data = form.cleaned_data
        if availability(data['check_in'], data['check_out']):
            booking = Booking.objects.create(
                user=self.request.user,
                check_in=data['check_in'],
                check_out=data['check_out'],
                number_of_guests=data['number_of_guests'],
                note=data['note'], )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('Tento termín už je rezervovaný')
        # form.print_form()
        # return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)

        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list


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


def booking_edit(request, booking_id=None):
    instance = Booking()
    if booking_id:
        instance = get_object_or_404(Booking, pk=booking_id)
    else:
        instance = Booking()

    form = BookingForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('chalupa:BookingView'))
    return render(request, 'chalupa/booking_edit.html', {'form': form})


class BookingCancelView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'chalupa/booking_cancel.html'
    success_url = reverse_lazy('chalupa:BookingView')


def gallery(request):
    category = request.GET.get('category')
    if category == None:
        images = Attachment.objects.all()
    else:
        images = Attachment.objects.filter(category__name=category)

    categories = Category.objects.all()
    context = {'categories': categories, 'images': images}
    return render(request, 'chalupa/gallery.html', context)


def view_image(request, pk):
    image = Attachment.objects.get(id=pk)
    return render(request, 'chalupa/gallery.html', {'image': image})


def add_image(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(title=data['category_new'])
        else:
            category = None

        attachment = Attachment.objects.create(
            title=data['title'],
            category=category,
            image=image,
        )

        return redirect('chalupa:Gallery')

    context = {'categories': categories}
    return render(request, 'chalupa/image_add.html', context)


'''class CalendarView(generic.ListView):
    model = Booking
    template_name = 'booking_view.html'
    '''
