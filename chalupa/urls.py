from django.urls import path
from . import views
#from .views import RoomListView, BookingView, RoomDetailView

app_name = 'chalupa'
urlpatterns = [
    path('', views.index, name='index'),
    path('pokoje/', views.RoomListView.as_view(), name='RoomListView'),
    path('pokoj/<int:pk>', views.RoomDetailView.as_view(), name='room-detail'),
    path('rezervovat/', views.BookingView.as_view(), name='BookingView'),
    path('rezervovat/upravit/<booking_id>', views.booking_edit, name='booking-edit'),
    path('rezervovat/zrusit/<pk>', views.BookingCancelView.as_view(), name='BookingCancelView'),
    path('galerie/', views.gallery, name='Gallery'),
    path('galerie/pridat', views.add_image, name='AddPhoto'),
    path('galerie/<str:pk>', views.view_image, name='Image'),

]
