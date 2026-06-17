"""
Security header and protection tests.
"""
from django.test import TestCase, override_settings


class SecurityHeadersTest(TestCase):
    def test_x_content_type_nosniff(self):
        resp = self.client.get("/")
        self.assertEqual(resp.get("X-Content-Type-Options"), "nosniff")

    def test_x_frame_options_deny(self):
        resp = self.client.get("/")
        self.assertEqual(resp.get("X-Frame-Options"), "DENY")

    def test_referrer_policy(self):
        resp = self.client.get("/")
        self.assertEqual(resp.get("Referrer-Policy"), "strict-origin-when-cross-origin")

    def test_permissions_policy(self):
        resp = self.client.get("/")
        self.assertIn("camera=()", resp.get("Permissions-Policy", ""))

    def test_xss_protection_header(self):
        resp = self.client.get("/")
        self.assertEqual(resp.get("X-XSS-Protection"), "1; mode=block")


class CSRFProtectionTest(TestCase):
    def test_post_without_csrf_rejected(self):
        # Django test client enforces CSRF by default only with enforce_csrf_checks=True
        client = self.client_class(enforce_csrf_checks=True)
        resp = client.post("/contact/", {
            "full_name": "Test",
            "email": "t@t.com",
            "subject": "Test",
            "message": "Test message.",
        })
        self.assertEqual(resp.status_code, 403)


class RateLimitTest(TestCase):
    def setUp(self):
        from core.middleware import _rate_store
        _rate_store.clear()

    def test_rate_limit_on_contact(self):
        """Exceeding 10 POSTs in 60s should get 429."""
        from core.middleware import _rate_store
        _rate_store.clear()

        data = {
            "full_name": "Attacker",
            "email": "a@a.com",
            "inquiry_type": "general",
            "subject": "Spam",
            "message": "Spam message content here.",
        }
        responses = []
        for _ in range(12):
            responses.append(self.client.post("/contact/", data))

        status_codes = [r.status_code for r in responses]
        self.assertIn(429, status_codes)


class AdminSecurityTest(TestCase):
    def test_admin_requires_auth(self):
        resp = self.client.get("/admin/")
        self.assertIn(resp.status_code, [302, 301])

    def test_dashboard_requires_auth(self):
        resp = self.client.get("/dashboard/")
        self.assertRedirects(resp, "/admin/login/?next=/dashboard/")


class InputValidationTest(TestCase):
    def test_xss_in_contact_form(self):
        """XSS payload in form fields should not execute."""
        data = {
            "full_name": "<script>alert('xss')</script>",
            "email": "xss@test.com",
            "inquiry_type": "general",
            "subject": "<img src=x onerror=alert(1)>",
            "message": "javascript:alert(1)",
        }
        resp = self.client.post("/contact/", data, follow=True)
        # Response should not contain raw unescaped script tags
        self.assertNotContains(resp, "<script>alert('xss')</script>")

    def test_sql_injection_in_search(self):
        """SQL injection attempt in query params should not cause 500."""
        resp = self.client.get("/projects/", {"category": "'; DROP TABLE projects; --"})
        self.assertNotEqual(resp.status_code, 500)

    def test_sql_injection_in_blog_search(self):
        resp = self.client.get("/blog/", {"q": "' OR '1'='1"})
        self.assertNotEqual(resp.status_code, 500)
