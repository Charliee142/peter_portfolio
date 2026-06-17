from django.contrib import admin
from .models import Booking, ConsultationSlot


@admin.register(ConsultationSlot)
class ConsultationSlotAdmin(admin.ModelAdmin):
    list_display = ['date', 'start_time', 'end_time', 'is_available']
    list_filter = ['is_available', 'date']
    list_editable = ['is_available']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'consultation_type', 'status', 'created_at']
    list_filter = ['status', 'consultation_type']
    search_fields = ['full_name', 'email']
