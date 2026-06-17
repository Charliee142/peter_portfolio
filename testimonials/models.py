from django.db import models


class Testimonial(models.Model):
    client_name = models.CharField(max_length=200)
    client_title = models.CharField(max_length=200, blank=True)
    client_company = models.CharField(max_length=200, blank=True)
    client_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5, help_text='1-5')
    service_type = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']

    def __str__(self):
        return f'{self.client_name} - {self.client_company}'
