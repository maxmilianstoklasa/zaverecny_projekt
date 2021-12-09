from django.db import models
from django.conf import settings
# from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse

# Create your models here.



def attachment_path(instance, filename):
    return "pokoj/" + str(instance.room.id) + "/attachments/" + filename


def image_path(instance, filename):
    return "pokoj/" + str(instance.id) + "/image/" + filename


'''class BookingObject(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name', help_text='Chalupa Stoklaska')
    image = models.ImageField(upload_to=image_path, blank=True, null=True, verbose_name='Image')
    address = models.CharField(max_length=100, verbose_name='Address', help_text='Ludvíkov 81')
    capacity = models.PositiveIntegerField(default='12', help_text='How many guests can be housed?')
    price_per_night = models.PositiveIntegerField(default='1000', verbose_name='Price per night',
                                                  help_text='The cost per one night')
    private_bathroom = models.BooleanField(verbose_name='Private bathroom',
                                           help_text='Does the guesthouse have a private bathroom?')
    number_of_rooms = models.PositiveIntegerField(default='3', verbose_name='Number of rooms',
                                                  help_text='How many rooms for guests does it have?')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]'''

class Room(models.Model):
    '''room_names = (
        ('modry', 'Modrý pokoj'),
        ('zeleny', 'Zelený pokoj'),
        ('oranzovy', 'Oranžový pokoj'),
    )'''
    name = models.CharField(max_length=20, verbose_name='Room name', help_text='Enter the room name')
    image = models.ImageField(upload_to=image_path, blank=True, null=True, verbose_name="Image")
    capacity = models.PositiveIntegerField(help_text='Enter the capacity of the room (extra beds included)', default='3')
    extra_bed = models.BooleanField(default=False)
    #booking_object = models.ForeignKey(BookingObject, on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]

    '''def get_absolute_url(self):
        return reverse('RoomDetailView', args=[str(self.id)])'''

    def __str__(self):
        return f'{self.name}, pro {self.capacity} osoby'


class Booking(models.Model):
    number_of_guests = models.IntegerField(default=1)
    check_in = models.DateField(verbose_name='Od', default='')
    check_out = models.DateField(verbose_name='Do', default='')
    note = models.TextField(max_length=2000, null=True, blank=True)
    #booking_object = models.ForeignKey(BookingObject, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, help_text='Enter the name and surname', on_delete=models.CASCADE,
                             default='')

    class Meta:
        ordering = ["user"]

    def __str__(self):
        return f'{self.user}, od {self.check_in} do {self.check_out}, {self.number_of_guests} hostů'

    @property
    def get_html_url(self):
        url = reverse('chalupa:booking-edit', args=(self.id,))
        return f'<a href="{url}"> Rezervováno od {self.user} </a>'


class Category(models.Model):
    name = models.CharField(max_length=40, null=False, blank=False)

    def __str__(self):
        return self.name


class Attachment(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    #last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=False, blank=False)
    #booking_object = models.ForeignKey(BookingObject, on_delete=models.CASCADE)
    #room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = 'title'
