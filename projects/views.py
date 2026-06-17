from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Project, ProjectCategory, Technology


def project_list(request):
    projects = Project.objects.all().prefetch_related('technologies')
    category_slug = request.GET.get('category')
    tech_filter = request.GET.get('tech')
    project_type = request.GET.get('type')

    if category_slug:
        projects = projects.filter(category__slug=category_slug)
    if tech_filter:
        projects = projects.filter(technologies__name__icontains=tech_filter)
    if project_type:
        projects = projects.filter(project_type=project_type)

    paginator = Paginator(projects, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'categories': ProjectCategory.objects.all(),
        'technologies': Technology.objects.all()[:20],
        'active_category': category_slug,
        'project_types': Project.TYPE_CHOICES,
        'active_type': project_type,
    }
    return render(request, 'projects/list.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related = Project.objects.filter(
        project_type=project.project_type
    ).exclude(id=project.id)[:3]
    context = {
        'project': project,
        'related_projects': related,
        'images': project.images.all(),
        'metrics': project.metrics.all(),
    }
    return render(request, 'projects/detail.html', context)
