from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from projects.models import Project
from blog.models import Post
from services.models import Service
from training.models import TrainingProgram


class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return ['core:home', 'core:about', 'contact:contact',
                'projects:list', 'blog:list', 'services:list', 'training:list']

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Project.objects.filter(status='completed')

    def lastmod(self, obj):
        return obj.updated_at


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at


class ServiceSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Service.objects.filter(is_active=True)


class TrainingSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return TrainingProgram.objects.filter(is_active=True)
