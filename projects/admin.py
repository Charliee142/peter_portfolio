from django.contrib import admin
from .models import Project, ProjectCategory, Technology, ProjectImage, ProjectMetric


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


class ProjectMetricInline(admin.TabularInline):
    model = ProjectMetric
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'project_type', 'status', 'is_featured', 'order', 'created_at']
    list_filter = ['status', 'project_type', 'is_featured']
    list_editable = ['is_featured', 'order']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['technologies']
    inlines = [ProjectImageInline, ProjectMetricInline]
    search_fields = ['title', 'short_description']


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']
    search_fields = ['name']
