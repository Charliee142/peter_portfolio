from django.db import models


class ConsultationSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    max_bookings = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['date', 'start_time']

    def __str__(self):
        return f'{self.date} {self.start_time}-{self.end_time}'


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    CONSULTATION_TYPES = [
        ('data_analysis', 'Data Analysis Consultation'),
        ('product_strategy', 'Product Strategy Session'),
        ('career_advice', 'Career Advice'),
        ('project_review', 'Project Review'),
        ('general', 'General Consultation'),
    ]

    slot = models.ForeignKey(ConsultationSlot, on_delete=models.SET_NULL, null=True, related_name='bookings')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)
    consultation_type = models.CharField(max_length=20, choices=CONSULTATION_TYPES, default='general')
    description = models.TextField(help_text='Briefly describe what you want to discuss')
    meeting_link = models.URLField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} - {self.consultation_type}'
