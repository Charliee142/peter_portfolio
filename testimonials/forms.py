from django import forms
from .models import Testimonial


class TestimonialForm(forms.ModelForm):

    class Meta:
        model = Testimonial

        fields = [
            "client_name",
            "client_title",
            "client_company",
            "client_image",
            "service_type",
            "rating",
            "content",
        ]

        widgets = {
            "client_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your Name"}
            ),
            "client_title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Job Title"}
            ),
            "client_company": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Company or Organization",
                }
            ),
            "service_type": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Django Development, Training, Cybersecurity...",
                }
            ),
            "rating": forms.Select(
                choices=[
                    (5, "⭐⭐⭐⭐⭐ Excellent"),
                    (4, "⭐⭐⭐⭐ Very Good"),
                    (3, "⭐⭐⭐ Good"),
                    (2, "⭐⭐ Fair"),
                    (1, "⭐ Poor"),
                ],
                attrs={"class": "form-select"},
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Tell others about your experience working or learning with Peter...",
                }
            ),
        }
