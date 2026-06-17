from django.contrib import admin
from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_company', 'rating', 'is_featured', 'is_approved']
    list_filter = ['is_featured', 'is_approved', 'rating']
    list_editable = ['is_featured', 'is_approved']
