"""
Tests for all portfolio forms.
"""
from django.test import TestCase
from contact.forms import ContactForm
from bookings.forms import BookingForm
from bookings.models import ConsultationSlot
from datetime import date, timedelta


class ContactFormTest(TestCase):
    def valid_data(self, **kwargs):
        data = {
            "full_name": "Amaka Obi",
            "email": "amaka@secureops.com",
            "inquiry_type": "service",
            "subject": "Penetration Test Request",
            "message": "We would like a penetration test for our banking API.",
        }
        data.update(kwargs)
        return data

    def test_valid_form(self):
        form = ContactForm(data=self.valid_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_missing_required_fields(self):
        for field in ("full_name", "email", "subject", "message"):
            data = self.valid_data()
            data[field] = ""
            form = ContactForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertIn(field, form.errors)

    def test_invalid_email(self):
        form = ContactForm(data=self.valid_data(email="not-an-email"))
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_optional_phone_and_company(self):
        data = self.valid_data()
        data.pop("phone", None)
        data.pop("company", None)
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_inquiry_type_choices(self):
        form = ContactForm(data=self.valid_data(inquiry_type="invalid_type"))
        self.assertFalse(form.is_valid())

    def test_form_widgets_have_cyber_class(self):
        form = ContactForm()
        self.assertIn("cyber-input", form.fields["full_name"].widget.attrs.get("class", ""))

    def test_save_creates_message(self):
        from contact.models import ContactMessage
        form = ContactForm(data=self.valid_data())
        self.assertTrue(form.is_valid())
        msg = form.save()
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(msg.full_name, "Amaka Obi")
        self.assertEqual(msg.status, "new")


class BookingFormTest(TestCase):
    def setUp(self):
        self.slot = ConsultationSlot.objects.create(
            date=date.today() + timedelta(days=7),
            start_time="10:00:00",
            end_time="11:00:00",
            is_available=True,
        )

    def valid_data(self, **kwargs):
        data = {
            "slot": self.slot.pk,
            "full_name": "Bello Usman",
            "email": "bello@test.com",
            "consultation_type": "general",
            "description": "I want to discuss a security assessment.",
        }
        data.update(kwargs)
        return data

    def test_valid_form(self):
        form = BookingForm(data=self.valid_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_missing_description(self):
        data = self.valid_data(description="")
        form = BookingForm(data=data)
        self.assertFalse(form.is_valid())

    def test_missing_email(self):
        data = self.valid_data(email="")
        form = BookingForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        data = self.valid_data(email="bad-email")
        form = BookingForm(data=data)
        self.assertFalse(form.is_valid())
