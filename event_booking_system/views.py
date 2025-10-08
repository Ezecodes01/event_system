from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from .models import Event, Ticket
from django.http import HttpRequest

def register(request : HttpRequest):
   error = None
   if request.method == "POST":
       username = request.POST.get("username")
       password1 = request.POST.get("password1")
       password2 = request.POST.get("password2")

       if password1 != password2 or len(password1) < 8 :
           error = 'Ensure both passwords match and password has at least 8 characters'

       else :
            try :
                user_exist = User.objects.filter(username = username).first()
                if user_exist :
                    error = 'User already exist for for this account'
                else :
                    user = User.objects.create_user(username = username,password=password1)

                    user.save()

                    return redirect("login")
            except Exception as e :
                error = str(e)        

   return render(request,'register.html', {"error" : error,})
# def register(request):
#     """User registration with auto-login after success."""
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("event_list")
#     else:
#         form = UserCreationForm()
#     return render(request, "register.html", {"form": form})


def event_list(request):
    """List all events ordered by start time."""
    events = Event.objects.all().order_by("start_time")
    return render(request, "event_list.html", {"events": events})


def event_detail(request, event_id):
    """Event detail page."""
    event = get_object_or_404(Event, id=event_id)
    return render(request, "event_detail.html", {"event": event})


@login_required
def book_ticket(request, event_id):
    """Book tickets for an event."""
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))

        if event.capacity >= quantity and quantity > 0:
            ticket = Ticket.objects.create(event=event, user=request.user, quantity=quantity)
            event.capacity -= quantity
            event.save()
            return redirect("booking_confirmation", ticket_id=ticket.id)

    return render(request, "book_ticket.html", {"event": event})


@login_required
def booking_confirmation(request, ticket_id):
    """Show confirmation page for a specific ticket."""
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    return render(request, "booking_confirmation.html", {"ticket": ticket})


@login_required
def my_bookings(request):
    """List all bookings for the logged-in user."""
    tickets = Ticket.objects.filter(user=request.user).select_related("event")
    return render(request, "my_bookings.html", {"tickets": tickets})

@login_required
def logout_view(request):
    """Log out the user."""
    logout(request)
    return redirect("login")
