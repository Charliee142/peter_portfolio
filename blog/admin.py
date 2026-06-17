from django.contrib import admin
from .models import *

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'is_featured', 'views_count', 'published_at']
    list_filter = ['status', 'is_featured', 'category']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    search_fields = ['title', 'content']
    inlines = [PostImageInline]


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Tag)
