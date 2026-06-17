from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'inquiry_type', 'subject', 'status', 'created_at']
    list_filter = ['status', 'inquiry_type']
    readonly_fields = ['created_at', 'ip_address']
    search_fields = ['full_name', 'email', 'subject']
