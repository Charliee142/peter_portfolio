"""
Tests for all URL patterns — resolves and status codes.
"""
from django.test import TestCase, Client
from django.urls import reverse, resolve


class URLResolutionTest(TestCase):
    """Ensure all named URLs resolve correctly."""

    def test_home_resolves(self):
        from core.views import home
        self.assertEqual(resolve("/").func, home)

    def test_about_resolves(self):
        from core.views import about
        self.assertEqual(resolve("/about/").func, about)

    def test_projects_list_resolves(self):
        url = reverse("projects:list")
        self.assertEqual(url, "/projects/")

    def test_blog_list_resolves(self):
        url = reverse("blog:list")
        self.assertEqual(url, "/blog/")

    def test_services_list_resolves(self):
        url = reverse("services:list")
        self.assertEqual(url, "/services/")

    def test_training_list_resolves(self):
        url = reverse("training:list")
        self.assertEqual(url, "/training/")

    def test_contact_resolves(self):
        url = reverse("contact:contact")
        self.assertEqual(url, "/contact/")

    def test_bookings_resolves(self):
        url = reverse("bookings:booking")
        self.assertEqual(url, "/bookings/")

    def test_dashboard_resolves(self):
        url = reverse("dashboard:home")
        self.assertEqual(url, "/dashboard/")

    def test_api_root_resolves(self):
        url = reverse("api:root")
        self.assertEqual(url, "/api/v1/")

    def test_api_projects_resolves(self):
        url = reverse("api:projects")
        self.assertEqual(url, "/api/v1/projects/")

    def test_robots_txt_resolves(self):
        url = reverse("robots_txt")
        self.assertEqual(url, "/robots.txt")

    def test_sitemap_resolves(self):
        url = reverse("sitemap")
        self.assertEqual(url, "/sitemap.xml")


class StaticPageStatusTest(TestCase):
    """All static pages should return 200."""

    def test_home_200(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_about_200(self):
        self.assertEqual(self.client.get("/about/").status_code, 200)

    def test_projects_200(self):
        self.assertEqual(self.client.get("/projects/").status_code, 200)

    def test_blog_200(self):
        self.assertEqual(self.client.get("/blog/").status_code, 200)

    def test_services_200(self):
        self.assertEqual(self.client.get("/services/").status_code, 200)

    def test_training_200(self):
        self.assertEqual(self.client.get("/training/").status_code, 200)

    def test_contact_200(self):
        self.assertEqual(self.client.get("/contact/").status_code, 200)

    def test_bookings_200(self):
        self.assertEqual(self.client.get("/bookings/").status_code, 200)

    def test_robots_200(self):
        self.assertEqual(self.client.get("/robots.txt").status_code, 200)

    def test_sitemap_200(self):
        self.assertEqual(self.client.get("/sitemap.xml").status_code, 200)

    def test_404_for_nonexistent_url(self):
        self.assertEqual(self.client.get("/this-page-does-not-exist/").status_code, 404)
