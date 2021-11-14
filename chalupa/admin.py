from django.contrib import admin
from .models import Room, Booking, Attachment
# Register your models here.
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Attachment)

# class RoomAdmin(admin.ModelAdmin):
#    list_display = ('capacity', 'extra_bed')
#    fields = ['user', 'email', 'number_of_guests', ('check_in', 'check_out'), 'note']


#admin.site.register(Room, RoomAdmin)


#@admin.register(Booking)
#class BookingAdmin(admin.ModelAdmin):
#    list_display = ('name', 'check_in', 'check_out', 'number_of_guests', 'phone_number')
