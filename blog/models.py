from django.db import models
from django.core.validators import FileExtensionValidator

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=100, default='Engineering')
    read_time = models.CharField(max_length=50, default='5 min read')
    image = models.ImageField(
        upload_to='blog/', blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])]
    )
    body = models.TextField(help_text="Markdown or HTML content")
    date_posted = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title
