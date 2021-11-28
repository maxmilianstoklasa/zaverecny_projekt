from django.urls import path
from .views import BookingList, RoomListView, BookingView, RoomDetailView
from . import views

app_name = 'chalupa'
urlpatterns = [
    path('', views.index, name='index'),
    path('seznam_rezervaci/', BookingList.as_view(), name='BookingList'),
    path('pokoje/', views.RoomListView.as_view(), name='RoomListView'),
    path('pokoj/<int:pk>', views.RoomDetailView.as_view(), name='room-detail'),
    path('rezervovat/', BookingView.as_view(), name='BookingView')
]