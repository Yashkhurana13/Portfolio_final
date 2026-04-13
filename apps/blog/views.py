from django.shortcuts import render, get_object_or_404
from .models import BlogPost


def blog_list(request):
    """Blog list page showing all published posts"""
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, 'blog_list.html', {'posts': posts})


def blog_detail(request, slug):
    """Blog detail page"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'blog_detail.html', {'post': post})
