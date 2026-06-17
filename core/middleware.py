"""
Security middleware — CSP, security headers, rate limiting.
"""
import logging
import time
from collections import defaultdict
from django.conf import settings
from django.http import HttpResponse
from django.utils.cache import patch_vary_headers

logger = logging.getLogger('django.security')

# Simple in-process rate limiter (per IP, contact/booking endpoints)
_rate_store: dict = defaultdict(list)
RATE_LIMIT = 10       # requests
RATE_WINDOW = 60      # seconds


def _build_csp(csp_dict: dict) -> str:
    parts = []
    for directive, sources in csp_dict.items():
        parts.append(f"{directive} {' '.join(sources)}")
    return "; ".join(parts)


class SecurityHeadersMiddleware:
    """Adds security headers to every response and applies per-IP rate limiting
    to sensitive endpoints."""

    RATE_LIMITED_PATHS = ('/contact/', '/bookings/')

    def __init__(self, get_response):
        self.get_response = get_response
        self._csp = _build_csp(getattr(settings, 'CSP_SETTINGS', {}))

    def __call__(self, request):
        # Rate limiting on sensitive paths
        if request.method == 'POST' and any(
            request.path.startswith(p) for p in self.RATE_LIMITED_PATHS
        ):
            ip = self._get_ip(request)
            now = time.time()
            timestamps = _rate_store[ip]
            _rate_store[ip] = [t for t in timestamps if now - t < RATE_WINDOW]
            if len(_rate_store[ip]) >= RATE_LIMIT:
                logger.warning(f"Rate limit exceeded for IP {ip} on {request.path}")
                return HttpResponse("Too many requests. Please wait a moment.", status=429, content_type="text/plain")
            _rate_store[ip].append(now)

        response = self.get_response(request)

        # Security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = (
            'camera=(), microphone=(), geolocation=(), payment=()'
        )
        response['X-XSS-Protection'] = '1; mode=block'

        if self._csp:
            response['Content-Security-Policy'] = self._csp

        patch_vary_headers(response, ['Accept-Encoding'])
        return response

    @staticmethod
    def _get_ip(request) -> str:
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            return xff.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '0.0.0.0')
