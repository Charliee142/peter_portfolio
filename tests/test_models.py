"""
Tests for all portfolio models.
Target: 80%+ coverage on model layer.
"""
from datetime import date, timedelta
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from core.models import SiteSettings, Skill, Experience, Education, Certification
from projects.models import Project, ProjectCategory, Technology, ProjectMetric
from blog.models import Post, BlogCategory, Tag
from services.models import Service
from training.models import TrainingProgram
from testimonials.models import Testimonial
from contact.models import ContactMessage
from bookings.models import Booking, ConsultationSlot


class SiteSettingsModelTest(TestCase):
    def setUp(self):
        self.settings = SiteSettings.objects.create(
            site_name="Peter Charles Portfolio",
            tagline="Cybersecurity Engineer",
            email="peter@petercharles.dev",
            location="Abuja, Nigeria",
            students_trained=200,
        )

    def test_str(self):
        self.assertEqual(str(self.settings), "Peter Charles Portfolio")

    def test_defaults(self):
        self.assertEqual(self.settings.years_experience, 5)
        self.assertEqual(self.settings.projects_completed, 30)


class SkillModelTest(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(
            name="Python", category="python", proficiency=92,
            icon_class="fab fa-python", is_featured=True,
        )

    def test_str(self):
        self.assertIn("Python", str(self.skill))
        self.assertIn("python", str(self.skill))

    def test_proficiency_range(self):
        self.assertGreaterEqual(self.skill.proficiency, 0)
        self.assertLessEqual(self.skill.proficiency, 100)

    def test_ordering(self):
        s2 = Skill.objects.create(name="Django", category="django", proficiency=88, order=1)
        skills = list(Skill.objects.all())
        self.assertEqual(skills[0], self.skill)


class ExperienceModelTest(TestCase):
    def setUp(self):
        self.exp = Experience.objects.create(
            title="Cybersecurity Engineer",
            company="SecureOps Africa",
            location="Abuja, Nigeria",
            start_date=date(2022, 3, 1),
            is_current=True,
            description="Lead security assessments.",
            technologies="Python,Django,Kali Linux",
        )

    def test_str(self):
        self.assertIn("Cybersecurity Engineer", str(self.exp))
        self.assertIn("SecureOps Africa", str(self.exp))

    def test_technologies_list_with_values(self):
        result = self.exp.technologies_list
        self.assertEqual(result, ["Python", "Django", "Kali Linux"])

    def test_technologies_list_empty(self):
        self.exp.technologies = ""
        self.exp.save()
        self.assertEqual(self.exp.technologies_list, [])

    def test_technologies_list_strips_whitespace(self):
        self.exp.technologies = " Python , Django , Burp Suite "
        self.exp.save()
        result = self.exp.technologies_list
        self.assertEqual(result, ["Python", "Django", "Burp Suite"])

    def test_duration_current(self):
        duration = self.exp.duration
        self.assertIsInstance(duration, str)
        self.assertTrue(len(duration) > 0)

    def test_duration_completed(self):
        exp = Experience.objects.create(
            title="Instructor",
            company="CyberSkills",
            start_date=date(2019, 1, 1),
            end_date=date(2021, 1, 1),
            is_current=False,
            description="Taught cybersecurity.",
        )
        # 2 years exactly
        self.assertIn("2", exp.duration)

    def test_duration_months_only(self):
        exp = Experience.objects.create(
            title="Consultant",
            company="TechBridge",
            start_date=date(2021, 1, 1),
            end_date=date(2021, 6, 30),
            is_current=False,
            description="Short engagement.",
        )
        self.assertIn("months", exp.duration)


class EducationModelTest(TestCase):
    def test_str(self):
        edu = Education.objects.create(
            institution="University of Abuja",
            degree="BSc Computer Science",
            field_of_study="Computer Science",
            start_year=2015, end_year=2019,
        )
        self.assertIn("BSc Computer Science", str(edu))
        self.assertIn("University of Abuja", str(edu))


class CertificationModelTest(TestCase):
    def test_str(self):
        cert = Certification.objects.create(
            name="CEH", issuing_org="EC-Council",
            issue_date=date(2021, 4, 15),
        )
        self.assertIn("CEH", str(cert))
        self.assertIn("EC-Council", str(cert))


class ProjectModelTest(TestCase):
    def setUp(self):
        self.cat = ProjectCategory.objects.create(name="Cybersecurity", slug="cybersecurity")
        self.tech = Technology.objects.create(name="Python")
        self.project = Project.objects.create(
            title="OSINT Toolkit",
            slug="osint-toolkit",
            project_type="automation",
            short_description="OSINT automation tool.",
            status="completed",
            is_featured=True,
        )
        self.project.technologies.add(self.tech)

    def test_str(self):
        self.assertEqual(str(self.project), "OSINT Toolkit")

    def test_auto_slug(self):
        p = Project.objects.create(
            title="New Security Project",
            short_description="Test.",
            project_type="web",
        )
        self.assertEqual(p.slug, "new-security-project")

    def test_get_absolute_url(self):
        url = self.project.get_absolute_url()
        self.assertIn("osint-toolkit", url)

    def test_technology_relation(self):
        self.assertIn(self.tech, self.project.technologies.all())

    def test_featured_ordering(self):
        p2 = Project.objects.create(
            title="Another Project", slug="another-project",
            short_description="Test.", project_type="web", is_featured=False,
        )
        projects = list(Project.objects.all())
        featured = [p for p in projects if p.is_featured]
        self.assertIn(self.project, featured)


class ServiceModelTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            title="Penetration Testing",
            slug="penetration-testing",
            short_description="Web app pen testing.",
            features="Scope definition\nVulnerability scanning\nExploitation",
            deliverables="Executive summary\nTechnical report\nRetest",
            price_from=250000,
            is_active=True,
        )

    def test_str(self):
        self.assertEqual(str(self.service), "Penetration Testing")

    def test_get_features_list(self):
        result = self.service.get_features_list()
        self.assertEqual(len(result), 3)
        self.assertIn("Scope definition", result)

    def test_get_deliverables_list(self):
        result = self.service.get_deliverables_list()
        self.assertEqual(len(result), 3)

    def test_empty_features(self):
        self.service.features = ""
        self.service.save()
        self.assertEqual(self.service.get_features_list(), [])


class TrainingProgramModelTest(TestCase):
    def test_str_and_slug(self):
        tp = TrainingProgram.objects.create(
            title="Ethical Hacking Bootcamp",
            level="beginner", delivery_mode="online",
            short_description="Learn ethical hacking.",
            duration_weeks=8, hours_per_week=12,
        )
        self.assertEqual(str(tp), "Ethical Hacking Bootcamp")
        self.assertEqual(tp.slug, "ethical-hacking-bootcamp")


class BlogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("testuser", password="pass")
        self.category = BlogCategory.objects.create(name="Cybersecurity", slug="cybersecurity")
        self.post = Post.objects.create(
            title="OWASP Top 10 Guide",
            slug="owasp-top-10-guide",
            author=self.user,
            category=self.category,
            excerpt="A guide to OWASP.",
            content="Detailed OWASP content here." * 50,
            status="published",
            published_at=timezone.now(),
        )

    def test_str(self):
        self.assertEqual(str(self.post), "OWASP Top 10 Guide")

    def test_get_absolute_url(self):
        url = self.post.get_absolute_url()
        self.assertIn("owasp-top-10-guide", url)

    def test_read_time_auto_calculated(self):
        self.assertGreater(self.post.read_time, 0)

    def test_only_published_visible(self):
        Post.objects.create(
            title="Draft Post", slug="draft-post",
            author=self.user, excerpt="Draft.",
            content="Draft content.", status="draft",
        )
        published = Post.objects.filter(status="published")
        self.assertEqual(published.count(), 1)


class ContactMessageModelTest(TestCase):
    def test_str(self):
        msg = ContactMessage.objects.create(
            full_name="Amaka Obi",
            email="amaka@test.com",
            subject="Security Audit Request",
            message="Please audit our platform.",
            inquiry_type="service",
        )
        self.assertIn("Amaka Obi", str(msg))
        self.assertIn("Security Audit Request"[:50], str(msg))

    def test_default_status(self):
        msg = ContactMessage.objects.create(
            full_name="Test User", email="t@t.com",
            subject="Test", message="Hello.",
        )
        self.assertEqual(msg.status, "new")


class BookingModelTest(TestCase):
    def setUp(self):
        self.slot = ConsultationSlot.objects.create(
            date=date.today() + timedelta(days=7),
            start_time="10:00:00",
            end_time="11:00:00",
            is_available=True,
        )

    def test_slot_str(self):
        self.assertIn("10:00", str(self.slot))

    def test_booking_str(self):
        booking = Booking.objects.create(
            slot=self.slot,
            full_name="Bello Usman",
            email="bello@test.com",
            consultation_type="general",
            description="Security consultation.",
        )
        self.assertIn("Bello Usman", str(booking))

    def test_default_status_pending(self):
        booking = Booking.objects.create(
            full_name="Test", email="t@t.com",
            consultation_type="general",
            description="Test.",
        )
        self.assertEqual(booking.status, "pending")
