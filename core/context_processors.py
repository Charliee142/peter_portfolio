from .models import SiteSettings

from django.conf import settings

def site_context(request):
    try:
        settings_obj = SiteSettings.objects.first()
    except Exception:
        settings_obj = None
    return {
        'site_settings': settings_obj,
        'SITE_NAME': 'Peter Charles Portfolio',
    }


def turnstile(request):
    return {"TURNSTILE_SITE_KEY": settings.TURNSTILE_SITE_KEY}
