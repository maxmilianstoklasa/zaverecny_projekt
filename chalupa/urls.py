from django.urls import path
from . import views
from .views import BookingList, RoomListView, BookingView, RoomDetailView

app_name = 'chalupa'
urlpatterns = [
    path('', views.index, name='index'),
    path('seznam_rezervaci/', BookingList.as_view(), name='BookingList'),
    path('pokoje/', views.RoomListView.as_view(), name='RoomListView'),
    path('pokoj/<int:pk>', views.RoomDetailView.as_view(), name='room-detail'),
    path('rezervovat/', BookingView.as_view(), name='BookingView'),
    path('rezervovat/upravit/<booking_id>', views.booking, name='booking-edit'),
    path('galerie/', views.gallery, name='Gallery'),
    path('galerie/pridat', views.add_image, name='AddPhoto'),
    path('galerie/<str:pk>', views.view_image, name='Image'),
    # path('calendar/', views.CalendarView.as_view(), name='calendar'),

]
