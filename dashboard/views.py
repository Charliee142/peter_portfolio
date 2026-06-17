from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from projects.models import Project
from blog.models import Post
from contact.models import ContactMessage
from bookings.models import Booking
from testimonials.models import Testimonial
from django.views.decorators.cache import never_cache

@staff_member_required
@never_cache
def dashboard_home(request):
    context = {
        'total_projects': Project.objects.count(),
        'total_posts': Post.objects.filter(status='published').count(),
        'new_messages': ContactMessage.objects.filter(status='new').count(),
        'pending_bookings': Booking.objects.filter(status='pending').count(),
        'recent_messages': ContactMessage.objects.order_by('-created_at')[:5],
        'recent_bookings': Booking.objects.order_by('-created_at')[:5],
        'projects': Project.objects.order_by('-created_at')[:5],
    }
    return render(request, 'dashboard/home.html', context)
