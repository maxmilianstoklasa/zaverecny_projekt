import datetime
from chalupa.models import Booking

# zjisteni dostupnosti objektu
def availability(check_in, check_out):
    availability_list=[] # seznam spravnych hodnot
    booking_list = Booking.objects.all()
    for booking in booking_list:
        if booking.check_in > check_out or booking.check_out < check_in:
            availability_list.append(True)
        else:
            availability_list.append(False)
        return all(availability_list)

