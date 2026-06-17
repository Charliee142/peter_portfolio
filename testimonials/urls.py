from django.urls import path
from .views import TestimonialListView,TestimonialCreateView, TestimonialThanksView

app_name = "testimonials"

urlpatterns = [
    path("", TestimonialListView.as_view(), name="list"),
    path("submit/", TestimonialCreateView.as_view(), name="submit"),
    path("thanks/", TestimonialThanksView.as_view(), name="thanks"),
]
