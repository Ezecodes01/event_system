from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.event_list, name="event_list"),
    path("event/<int:event_id>/", views.event_detail, name='event_detail'),
    path("event/<int:event_id>/book/", views.book_ticket, name='book_ticket'),
    path("booking/<int:ticket_id>/confirmation/", views.booking_confirmation, name='booking_confirmation'),
    path("my-bookings/", views.my_bookings, name='my_bookings')
]
