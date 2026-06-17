from django.shortcuts import render, get_object_or_404
from .models import Service


def service_list(request):
    services = Service.objects.filter(is_active=True)
    context = {'services': services, 'featured': services.filter(is_featured=True)}
    return render(request, 'services/list.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    context = {'service': service, 'other_services': Service.objects.filter(is_active=True).exclude(id=service.id)[:4]}
    return render(request, 'services/detail.html', context)
