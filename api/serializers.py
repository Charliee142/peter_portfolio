from rest_framework import serializers
from projects.models import Project, Technology
from blog.models import Post
from services.models import Service


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ['id', 'name', 'icon_class', 'color']


class ProjectSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True, read_only=True)
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'project_type', 'status', 'short_description',
            'overview', 'technologies', 'demo_url', 'github_url',
            'is_featured', 'start_date', 'end_date', 'created_at', 'absolute_url'
        ]

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.get_absolute_url())
        return obj.get_absolute_url()


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'excerpt', 'author_name', 'published_at', 'read_time', 'views_count']

    def get_author_name(self, obj):
        return obj.author.get_full_name() or obj.author.username


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'slug', 'short_description', 'price_from', 'duration', 'is_featured']
