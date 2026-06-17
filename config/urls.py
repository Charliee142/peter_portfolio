from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import (
    StaticViewSitemap, ProjectSitemap, BlogSitemap,
    ServiceSitemap, TrainingSitemap,
)
from core.views import robots_txt

sitemaps = {
    'static': StaticViewSitemap,
    'projects': ProjectSitemap,
    'blog': BlogSitemap,
    'services': ServiceSitemap,
    'training': TrainingSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("projects/", include("projects.urls", namespace="projects")),
    path("blog/", include("blog.urls", namespace="blog")),
    path("services/", include("services.urls", namespace="services")),
    path("training/", include("training.urls", namespace="training")),
    path("contact/", include("contact.urls", namespace="contact")),
    path("bookings/", include("bookings.urls", namespace="bookings")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path("testimonials/", include("testimonials.urls")),
    path("api/v1/", include("api.urls", namespace="api")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
]

handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
