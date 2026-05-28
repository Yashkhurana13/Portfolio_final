from django.shortcuts import render, get_object_or_404, redirect
from django.utils.html import escape
from django.views.decorators.cache import cache_page
from .models import Post
from core.models import Profile
from django.core.paginator import Paginator
import logging

logger = logging.getLogger(__name__)

@cache_page(60 * 5)  # Cache for 5 minutes
def blog_view(request):
    # Redirect legacy ?slug= URLs to clean /<slug>/ URLs
    slug_param = request.GET.get('slug')
    if slug_param:
        return redirect('blog_detail', slug=slug_param, permanent=True)

    profile = Profile.objects.first()
    posts = Post.objects.filter(is_published=True)
    
    # Search functionality with input sanitization
    search_query = request.GET.get('search', '')
    if search_query:
        # Sanitize search input
        search_query = escape(search_query.strip())
        
        # Validate search query length
        if len(search_query) > 200:
            search_query = search_query[:200]
        
        # Use Django's ORM (protected against SQL injection)
        posts = posts.filter(title__icontains=search_query) | posts.filter(body__icontains=search_query)
        logger.info(f"Blog search executed: {search_query}")
    
    # Pagination - 9 posts per page
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    
    # Validate page number
    try:
        page_number = int(page_number) if page_number else 1
        if page_number < 1:
            page_number = 1
    except (ValueError, TypeError):
        page_number = 1
    
    page_obj = paginator.get_page(page_number)
    
    context = {
        'profile': profile,
        'posts': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'blog/blog.html', context)


def blog_detail_view(request, slug):
    """Clean URL single-post view at /blog/<slug>/"""
    post = get_object_or_404(Post, slug=slug, is_published=True)
    profile = Profile.objects.first()
    
    # Fetch up to 3 related posts by category
    related_posts_qs = Post.objects.filter(
        category=post.category, 
        is_published=True
    ).exclude(id=post.id).order_by('-date_posted')[:3]
    
    related_posts = list(related_posts_qs)
    
    # If not enough, fill with latest posts
    if len(related_posts) < 3:
        existing_ids = [p.id for p in related_posts] + [post.id]
        more_posts = Post.objects.filter(
            is_published=True
        ).exclude(id__in=existing_ids).order_by('-date_posted')[:3 - len(related_posts)]
        related_posts.extend(list(more_posts))

    context = {
        'profile': profile,
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)
