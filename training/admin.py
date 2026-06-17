from django.contrib import admin
from .models import TrainingProgram


@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'delivery_mode', 'price', 'is_active', 'is_featured']
    list_filter = ['level', 'delivery_mode', 'is_active', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
