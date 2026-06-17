from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    icon_class = models.CharField(max_length=100, default='fas fa-chart-bar')
    short_description = models.TextField(max_length=300)
    full_description = models.TextField(blank=True)
    features = models.TextField(blank=True, help_text='One feature per line')
    deliverables = models.TextField(blank=True, help_text='One deliverable per line')
    price_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def get_features_list(self):
        return [f.strip() for f in self.features.splitlines() if f.strip()]

    def get_deliverables_list(self):
        return [d.strip() for d in self.deliverables.splitlines() if d.strip()]
