import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import SiteSettings, Skill, Experience, Education, Certification
from projects.models import Project
from blog.models import Post
from services.models import Service
from testimonials.models import Testimonial
from training.models import TrainingProgram

logger = logging.getLogger('portfolio')


def get_site_settings():
    try:
        return SiteSettings.objects.first()
    except Exception:
        return None


def home(request):
    context = {
        'settings_obj': get_site_settings(),
        'featured_projects': Project.objects.filter(is_featured=True).prefetch_related('technologies')[:6],
        'featured_posts': Post.objects.filter(status='published', is_featured=True).select_related('category')[:3],
        'featured_services': Service.objects.filter(is_featured=True, is_active=True)[:4],
        'testimonials': Testimonial.objects.filter(is_featured=True, is_approved=True)[:6],
        'skills': Skill.objects.filter(is_featured=True)[:12],
        'stats': {
            'projects': Project.objects.filter(status='completed').count() or 30,
            'clients': Testimonial.objects.count() or 20,
            'experience': 5,
            'students': SiteSettings.objects.values_list('students_trained', flat=True).first() or 200,
        },
        # SEO
        'page_title': 'Peter Charles | Cybersecurity Engineer & Django Developer',
        'page_description': (
            'Peter Charles — Cybersecurity Engineer, Python & Django Developer, OSINT Researcher, '
            'and Ethical Hacking Instructor based in Abuja, Nigeria. Building secure digital solutions.'
        ),
        'og_type': 'website',
    }
    return render(request, 'core/home.html', context)


def about(request):
    skills = Skill.objects.all()
    skills_by_category: dict = {}
    for skill in skills:
        cat = skill.get_category_display()
        skills_by_category.setdefault(cat, []).append(skill)

    context = {
        'settings_obj': get_site_settings(),
        'skills': skills,
        'skills_by_category': skills_by_category,
        'experiences': Experience.objects.all(),
        'educations': Education.objects.all(),
        'certifications': Certification.objects.all(),
        'page_title': 'About Peter Charles | Cybersecurity Engineer & Django Developer',
        'page_description': (
            'Learn about Peter Charles — his expertise in cybersecurity, Python development, '
            'Django web apps, OSINT research, and technical training in Abuja, Nigeria.'
        ),
    }
    return render(request, 'core/about.html', context)


def robots_txt(request):
    site_url = getattr(settings, 'SITE_URL', 'https://petercharles.dev')
    content = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /dashboard/
Disallow: /api/

Sitemap: {site_url}/sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')


def csrf_failure(request, reason=''):
    logger.warning(f"CSRF failure: {reason} | IP: {request.META.get('REMOTE_ADDR')}")
    return render(request, 'errors/403.html', {'reason': reason}, status=403)


def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def error_500(request):
    return render(request, 'errors/500.html', status=500)
