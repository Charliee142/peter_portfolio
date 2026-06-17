from django.contrib import admin
from .models import SiteSettings, Skill, Experience, Education, Certification


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'tagline', 'email', 'location']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'is_featured', 'order']
    list_filter = ['category', 'is_featured']
    list_editable = ['order', 'is_featured']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'start_year', 'end_year']


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'issuing_org', 'issue_date', 'is_featured']
    list_filter = ['is_featured']
