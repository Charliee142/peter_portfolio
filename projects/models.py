from django.db import models
from django.utils.text import slugify


class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon_class = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=20, default='#00D9FF')

    class Meta:
        verbose_name_plural = 'Technologies'
        ordering = ['name']

    def __str__(self):
        return self.name


class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = 'Project Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('planned', 'Planned'),
        ('archived', 'Archived'),
    ]
    TYPE_CHOICES = [
        ('data', 'Data Analytics'),
        ('product', 'Product Management'),
        ('dashboard', 'Dashboard'),
        ('automation', 'Automation'),
        ('research', 'Research'),
        ('web', 'Web Application'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    project_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='data')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    short_description = models.TextField(max_length=500)
    
    # Case Study Fields
    overview = models.TextField(blank=True)
    problem_statement = models.TextField(blank=True)
    objectives = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    architecture = models.TextField(blank=True)
    database_design = models.TextField(blank=True)
    features = models.TextField(blank=True)
    challenges = models.TextField(blank=True)
    solutions = models.TextField(blank=True)
    lessons_learned = models.TextField(blank=True)
    future_improvements = models.TextField(blank=True)

    technologies = models.ManyToManyField(Technology, blank=True)
    
    featured_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    demo_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    documentation_url = models.URLField(blank=True)

    is_featured = models.BooleanField(default=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('projects:detail', kwargs={'slug': self.slug})


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_screenshot = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.project.title} - Image {self.order}'


class ProjectMetric(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='metrics')
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.project.title} - {self.label}: {self.value}'
