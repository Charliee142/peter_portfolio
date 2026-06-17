from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Post, BlogCategory, Tag
from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_page, never_cache


@require_GET
@cache_page(60 * 15)
def post_list(request):
    posts = Post.objects.filter(status='published').select_related('author', 'category')
    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')
    query = request.GET.get('q')

    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    if query:
        posts = posts.filter(title__icontains=query) | posts.filter(content__icontains=query)

    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    context = {
        'page_obj': page_obj,
        'categories': BlogCategory.objects.all(),
        'popular_posts': Post.objects.filter(status='published').order_by('-views_count')[:5],
        'active_category': category_slug,
    }
    return render(request, 'blog/list.html', context)


@require_GET
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    post.views_count += 1
    post.save(update_fields=['views_count'])
    related = Post.objects.filter(
        status='published', category=post.category
    ).exclude(id=post.id)[:3]
    context = {'post': post, 'related_posts': related}
    return render(request, 'blog/detail.html', context)
