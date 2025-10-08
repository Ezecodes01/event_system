from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Event(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    category = models.CharField(max_length=100, choices=[
        ('music', 'Music'),
        ('tech', 'Tech'),
        ('sports', 'Sports'),
        ('education', 'Education'),
    ])
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    capacity = models.PositiveIntegerField()
    background_image = models.ImageField(upload_to='event_backgrounds/', blank=True, null=True)

    def __str__(self):
        return self.title


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    quantity = models.PositiveIntegerField(default=1)
    booking_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    attendee_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

