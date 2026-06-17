from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'price_from', 'is_featured', 'is_active', 'order']
    list_filter = ['is_featured', 'is_active']
    list_editable = ['is_featured', 'order']
    prepopulated_fields = {'slug': ('title',)}
