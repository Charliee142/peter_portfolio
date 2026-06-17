from django.db import models
from django.utils.text import slugify


class TrainingProgram(models.Model):
    LEVEL_CHOICES = [('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')]
    DELIVERY_CHOICES = [('online', 'Online'), ('in_person', 'In-Person'), ('hybrid', 'Hybrid')]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='beginner')
    delivery_mode = models.CharField(max_length=15, choices=DELIVERY_CHOICES, default='online')
    short_description = models.TextField(max_length=300)
    full_description = models.TextField(blank=True)
    curriculum = models.TextField(blank=True, help_text='Markdown or HTML')
    duration_weeks = models.PositiveIntegerField(default=4)
    hours_per_week = models.PositiveIntegerField(default=5)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_participants = models.PositiveIntegerField(default=20)
    prerequisites = models.TextField(blank=True)
    tools_used = models.CharField(max_length=500, blank=True)
    certificate_offered = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    icon_class = models.CharField(max_length=100, default='fas fa-graduation-cap')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
