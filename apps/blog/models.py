from django.db import models
from django.utils.text import slugify


class BlogPost(models.Model):
    """Blog posts with publish/unpublish functionality"""
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=250, blank=True)
    excerpt = models.TextField(help_text='Short description for list view')
    content = models.TextField(help_text='Full blog content (supports HTML)')
    featured_image = models.ImageField(upload_to='blog/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
