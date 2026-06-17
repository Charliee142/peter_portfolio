from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from projects.models import Project
from blog.models import Post
from services.models import Service
from .serializers import ProjectSerializer, PostSerializer, ServiceSerializer


@api_view(['GET'])
def api_root(request):
    return Response({
        'projects': request.build_absolute_uri('/api/v1/projects/'),
        'posts': request.build_absolute_uri('/api/v1/posts/'),
        'services': request.build_absolute_uri('/api/v1/services/'),
    })


class ProjectListAPIView(generics.ListAPIView):
    queryset = Project.objects.all().prefetch_related('technologies')
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'short_description']
    ordering_fields = ['created_at', 'title']


class ProjectDetailAPIView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'slug'


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.filter(status='published')
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'excerpt']


class ServiceListAPIView(generics.ListAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
