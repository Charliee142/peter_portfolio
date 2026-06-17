"""
Tests for all portfolio views.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from core.models import SiteSettings, Skill
from projects.models import Project, ProjectCategory
from blog.models import Post, BlogCategory
from services.models import Service
from training.models import TrainingProgram
from testimonials.models import Testimonial


def make_user(username="peter", superuser=False):
    u = User.objects.create_user(username, email=f"{username}@test.com", password="testpass123")
    if superuser:
        u.is_staff = True; u.is_superuser = True; u.save()
    return u


class HomeViewTest(TestCase):
    def test_home_200(self):
        resp = self.client.get(reverse("core:home"))
        self.assertEqual(resp.status_code, 200)

    def test_home_uses_correct_template(self):
        resp = self.client.get(reverse("core:home"))
        self.assertTemplateUsed(resp, "core/home.html")
        self.assertTemplateUsed(resp, "base.html")

    def test_home_context_keys(self):
        resp = self.client.get(reverse("core:home"))
        for key in ("featured_projects", "featured_services", "testimonials", "stats"):
            self.assertIn(key, resp.context)

    def test_home_with_featured_data(self):
        Project.objects.create(
            title="Test Project", slug="test-project",
            short_description="Test.", is_featured=True, project_type="web",
        )
        Service.objects.create(
            title="Pen Test", slug="pen-test",
            short_description="Security testing.", is_featured=True, is_active=True,
        )
        resp = self.client.get(reverse("core:home"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Test Project")


class AboutViewTest(TestCase):
    def test_about_200(self):
        resp = self.client.get(reverse("core:about"))
        self.assertEqual(resp.status_code, 200)

    def test_about_template(self):
        resp = self.client.get(reverse("core:about"))
        self.assertTemplateUsed(resp, "core/about.html")

    def test_about_context(self):
        resp = self.client.get(reverse("core:about"))
        for key in ("skills", "experiences", "educations", "certifications"):
            self.assertIn(key, resp.context)

    def test_about_skills_by_category(self):
        Skill.objects.create(name="Python", category="python", proficiency=90)
        Skill.objects.create(name="Burp Suite", category="cybersecurity", proficiency=82)
        resp = self.client.get(reverse("core:about"))
        self.assertIn("skills_by_category", resp.context)
        self.assertGreater(len(resp.context["skills_by_category"]), 0)


class ProjectViewsTest(TestCase):
    def setUp(self):
        self.cat = ProjectCategory.objects.create(name="Cybersecurity", slug="cybersecurity")
        self.project = Project.objects.create(
            title="OSINT Toolkit",
            slug="osint-toolkit",
            project_type="automation",
            short_description="OSINT automation.",
            overview="Full overview.",
            problem_statement="The problem.",
            status="completed",
        )

    def test_project_list_200(self):
        resp = self.client.get(reverse("projects:list"))
        self.assertEqual(resp.status_code, 200)

    def test_project_list_shows_projects(self):
        resp = self.client.get(reverse("projects:list"))
        self.assertContains(resp, "OSINT Toolkit")

    def test_project_detail_200(self):
        resp = self.client.get(reverse("projects:detail", kwargs={"slug": "osint-toolkit"}))
        self.assertEqual(resp.status_code, 200)

    def test_project_detail_404(self):
        resp = self.client.get(reverse("projects:detail", kwargs={"slug": "nonexistent"}))
        self.assertEqual(resp.status_code, 404)

    def test_project_detail_context(self):
        resp = self.client.get(reverse("projects:detail", kwargs={"slug": "osint-toolkit"}))
        self.assertIn("project", resp.context)
        self.assertEqual(resp.context["project"].title, "OSINT Toolkit")

    def test_project_list_category_filter(self):
        resp = self.client.get(reverse("projects:list"), {"category": "cybersecurity"})
        self.assertEqual(resp.status_code, 200)

    def test_project_list_pagination(self):
        for i in range(12):
            Project.objects.create(
                title=f"Project {i}", slug=f"project-{i}",
                short_description="Test.", project_type="web",
            )
        resp = self.client.get(reverse("projects:list"))
        self.assertIn("page_obj", resp.context)


class BlogViewsTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.cat = BlogCategory.objects.create(name="Cybersecurity", slug="cybersecurity")
        self.post = Post.objects.create(
            title="OWASP Guide",
            slug="owasp-guide",
            author=self.user,
            category=self.cat,
            excerpt="OWASP overview.",
            content="Content " * 100,
            status="published",
            published_at=timezone.now(),
        )

    def test_post_list_200(self):
        resp = self.client.get(reverse("blog:list"))
        self.assertEqual(resp.status_code, 200)

    def test_post_list_only_published(self):
        Post.objects.create(
            title="Draft Post", slug="draft-post",
            author=self.user, excerpt="Draft.",
            content="Content.", status="draft",
        )
        resp = self.client.get(reverse("blog:list"))
        self.assertContains(resp, "OWASP Guide")
        self.assertNotContains(resp, "Draft Post")

    def test_post_detail_200(self):
        resp = self.client.get(reverse("blog:detail", kwargs={"slug": "owasp-guide"}))
        self.assertEqual(resp.status_code, 200)

    def test_post_detail_increments_views(self):
        initial = self.post.views_count
        self.client.get(reverse("blog:detail", kwargs={"slug": "owasp-guide"}))
        self.post.refresh_from_db()
        self.assertEqual(self.post.views_count, initial + 1)

    def test_post_detail_404_for_draft(self):
        Post.objects.create(
            title="Secret Draft", slug="secret-draft",
            author=self.user, excerpt="Secret.",
            content="Secret content.", status="draft",
        )
        resp = self.client.get(reverse("blog:detail", kwargs={"slug": "secret-draft"}))
        self.assertEqual(resp.status_code, 404)


class ServiceViewsTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            title="Penetration Testing",
            slug="penetration-testing",
            short_description="Web app pen testing.",
            features="Recon\nScanning\nExploitation",
            deliverables="Report\nRetest",
            price_from=250000,
            is_active=True,
            is_featured=True,
        )

    def test_service_list_200(self):
        resp = self.client.get(reverse("services:list"))
        self.assertEqual(resp.status_code, 200)

    def test_service_list_shows_active(self):
        resp = self.client.get(reverse("services:list"))
        self.assertContains(resp, "Penetration Testing")

    def test_service_detail_200(self):
        resp = self.client.get(reverse("services:detail", kwargs={"slug": "penetration-testing"}))
        self.assertEqual(resp.status_code, 200)

    def test_inactive_service_returns_404(self):
        Service.objects.create(
            title="Old Service", slug="old-service",
            short_description="Old.", is_active=False,
        )
        resp = self.client.get(reverse("services:detail", kwargs={"slug": "old-service"}))
        self.assertEqual(resp.status_code, 404)


class ContactViewTest(TestCase):
    def setUp(self):
        from core.middleware import _rate_store
        _rate_store.clear()

    def test_contact_get_200(self):
        resp = self.client.get(reverse("contact:contact"))
        self.assertEqual(resp.status_code, 200)

    def test_contact_post_valid(self):
        data = {
            "full_name": "Amaka Obi",
            "email": "amaka@test.com",
            "inquiry_type": "service",
            "subject": "Security Audit",
            "message": "Please audit our platform. This is a longer message to pass validation.",
        }
        resp = self.client.post(reverse("contact:contact"), data, follow=True)
        self.assertEqual(resp.status_code, 200)
        from contact.models import ContactMessage
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(ContactMessage.objects.first().full_name, "Amaka Obi")

    def test_contact_post_invalid(self):
        resp = self.client.post(reverse("contact:contact"), {"full_name": ""})
        self.assertEqual(resp.status_code, 200)
        from contact.models import ContactMessage
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_contact_post_htmx_returns_partial(self):
        data = {
            "full_name": "Test User",
            "email": "t@t.com",
            "inquiry_type": "general",
            "subject": "Test subject",
            "message": "This is a test message that is long enough.",
        }
        resp = self.client.post(
            reverse("contact:contact"), data,
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(resp.status_code, 200)


class DashboardViewTest(TestCase):
    def test_dashboard_requires_staff(self):
        resp = self.client.get(reverse("dashboard:home"))
        self.assertRedirects(resp, f"/admin/login/?next=/dashboard/")

    def test_dashboard_accessible_to_staff(self):
        u = make_user("staff", superuser=True)
        self.client.force_login(u)
        resp = self.client.get(reverse("dashboard:home"))
        self.assertEqual(resp.status_code, 200)


class RobotsTxtTest(TestCase):
    def test_robots_txt_200(self):
        resp = self.client.get("/robots.txt")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "text/plain")

    def test_robots_blocks_admin(self):
        resp = self.client.get("/robots.txt")
        self.assertIn(b"Disallow: /admin/", resp.content)

    def test_robots_includes_sitemap(self):
        resp = self.client.get("/robots.txt")
        self.assertIn(b"sitemap.xml", resp.content)


class APIViewsTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="API Test Project", slug="api-test-project",
            short_description="For API testing.", project_type="web", status="completed",
        )

    def test_api_root_200(self):
        resp = self.client.get(reverse("api:root"))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("projects", data)

    def test_projects_api_list(self):
        resp = self.client.get(reverse("api:projects"))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("results", data)

    def test_project_api_detail(self):
        resp = self.client.get(reverse("api:project-detail", kwargs={"slug": "api-test-project"}))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["title"], "API Test Project")
