from django.views.generic import ListView, CreateView, TemplateView
from rest_framework import settings

from core.utils.turnstile import verify_turnstile
from .models import Testimonial
from django.contrib import messages
from django.conf import settings
from django.urls import reverse_lazy
from .models import Testimonial
from .forms import TestimonialForm
from django.core.mail import send_mail

class TestimonialListView(ListView):
    model = Testimonial
    template_name = "testimonials/testimonial_list.html"
    context_object_name = "testimonials"
    paginate_by = 12

    def get_queryset(self):
        return Testimonial.objects.filter(is_approved=True)


class TestimonialCreateView(CreateView):

    model = Testimonial

    form_class = TestimonialForm

    template_name = "testimonials/testimonial_form.html"

    success_url = reverse_lazy("testimonials:thanks")

    def form_valid(self, form):

        token = self.request.POST.get("cf-turnstile-response")
        if not token:
            messages.error(
                self.request,
                "Please complete the CAPTCHA verification."
            )
            return self.form_invalid(form)

        if not verify_turnstile(token):
            messages.error(
                self.request,
                "CAPTCHA verification failed."
            )
            return self.form_invalid(form)

        testimonial = form.save(commit=False)

        testimonial.is_approved = False

        testimonial.save()

        send_mail(
            subject="New Testimonial Submitted",
            message=f"A new testimonial has been submitted by {testimonial.client_name}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
        )

        messages.success(
            self.request,
            "Thank you! Your testimonial has been submitted and is awaiting approval.",
        )

        return super().form_valid(form)


class TestimonialThanksView(TemplateView):
    template_name = "testimonials/thanks.html"
