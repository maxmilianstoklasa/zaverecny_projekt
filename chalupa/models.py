from django.db import models
from django.conf import settings
# from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


def attachment_path(instance, filename):
    return "pokoj/" + str(instance.room.id) + "/attachments/" + filename


def image_path(instance, filename):
    return "pokoj/" + str(instance.id) + "/image/" + filename


class Room(models.Model):
    room_names = (
        ('modry', 'Modrý pokoj'),
        ('zeleny', 'Zelený pokoj'),
        ('oranzovy', 'Oranžový pokoj'),
    )
    name = models.CharField(max_length=20, verbose_name='Room name', help_text='Enter the room name', choices=room_names)
    image = models.ImageField(upload_to=image_path, blank=True, null=True, verbose_name="Image")
    capacity = models.PositiveIntegerField(help_text='Enter the capacity of the room (extra beds included)', default='3')
    extra_bed = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f'{self.name}, pro {self.capacity} osoby'


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, help_text='Enter the name and surname', on_delete=models.CASCADE,
                             default='')
    number_of_guests = models.IntegerField(default=1)
    check_in = models.DateField(verbose_name='Od', blank=True, null=True)
    check_out = models.DateField(verbose_name='Do', blank=True, null=True)
    note = models.TextField(max_length=2000, null=True, blank=True)

    class Meta:
        ordering = ["user"]

    def __str__(self):
        return f'{self.user}, od {self.check_in} do {self.check_out}, {self.number_of_guests} hostů'


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    #phone_number = PhoneNumberField(unique=True, null=False, blank=False, default='+420',
     #                                 help_text='Enter the phone number (nine numbers in a row without spaces)')


class Attachment(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    last_update = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to=attachment_path, null=True, verbose_name="File")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        order_with_respect_to = 'room'

    def __str__(self):
        return f'{self.title}'