from django.db import models
from django.utils import timezone


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='Peter Charles Portfolio')
    tagline = models.CharField(max_length=255, default='Cybersecurity Engineer & Django Developer')
    about_short = models.TextField(blank=True)
    about_full = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True, default='Abuja, Nigeria')
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    resume_file = models.FileField(upload_to='resume/', blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    years_experience = models.PositiveIntegerField(default=5)
    projects_completed = models.PositiveIntegerField(default=30)
    clients_served = models.PositiveIntegerField(default=20)
    certifications_count = models.PositiveIntegerField(default=10)
    students_trained = models.PositiveIntegerField(default=100)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('cybersecurity', 'Cybersecurity'),
        ('python', 'Python Development'),
        ('django', 'Django & Web'),
        ('osint', 'OSINT & Recon'),
        ('tools', 'Tools & Platforms'),
        ('soft', 'Soft Skills'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    proficiency = models.PositiveIntegerField(default=80, help_text='0-100')
    icon_class = models.CharField(max_length=100, blank=True, help_text='FontAwesome or Devicon class')
    color = models.CharField(max_length=20, default='#00D9FF')
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.name} ({self.category})'


class Experience(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    technologies = models.CharField(max_length=500, blank=True,
                                    help_text='Comma-separated list of technologies')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.title} at {self.company}'

    @property
    def technologies_list(self):
        """Return technologies as a clean list. Fixes template split syntax error."""
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]
        return []

    @property
    def duration(self):
        end = self.end_date or timezone.now().date()
        months = (end.year - self.start_date.year) * 12 + (end.month - self.start_date.month)
        if months < 12:
            return f'{months} months'
        years = months // 12
        rem = months % 12
        return f'{years}y {rem}m' if rem else f'{years} years'


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    gpa = models.CharField(max_length=10, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-start_year']

    def __str__(self):
        return f'{self.degree} - {self.institution}'


class Certification(models.Model):
    name = models.CharField(max_length=200)
    issuing_org = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=200, blank=True)
    credential_url = models.URLField(blank=True)
    badge_image = models.ImageField(upload_to='certifications/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f'{self.name} - {self.issuing_org}'
