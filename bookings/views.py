from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Booking, ConsultationSlot
from .forms import BookingForm


def booking(request):
    slots = ConsultationSlot.objects.filter(is_available=True).order_by('date', 'start_time')
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consultation booked! You will receive a confirmation email.')
            return redirect('bookings:booking')
    else:
        form = BookingForm()
    context = {'form': form, 'slots': slots}
    return render(request, 'bookings/booking.html', context)
