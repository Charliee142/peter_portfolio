from django.db import models


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ]
    INQUIRY_CHOICES = [
        ('general', 'General Inquiry'),
        ('project', 'Project Collaboration'),
        ('service', 'Service Request'),
        ('training', 'Training Inquiry'),
        ('consulting', 'Consulting'),
        ('other', 'Other'),
    ]

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_CHOICES, default='general')
    subject = models.CharField(max_length=300)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} - {self.subject[:50]}'
