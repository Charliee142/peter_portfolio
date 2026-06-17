from django.shortcuts import render, get_object_or_404
from .models import TrainingProgram


def training_list(request):
    programs = TrainingProgram.objects.filter(is_active=True)
    context = {'programs': programs, 'featured': programs.filter(is_featured=True)}
    return render(request, 'training/list.html', context)


def training_detail(request, slug):
    program = get_object_or_404(TrainingProgram, slug=slug, is_active=True)
    context = {'program': program}
    return render(request, 'training/detail.html', context)
