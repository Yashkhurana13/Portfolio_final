from django.db import models
from django.core.validators import FileExtensionValidator
from io import BytesIO
from PIL import Image
from django.core.files import File

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, db_index=True)
    category = models.CharField(max_length=100, default='Engineering', db_index=True)
    read_time = models.CharField(max_length=50, default='5 min read')
    image = models.ImageField(
        upload_to='blog/', blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])]
    )
    body = models.TextField(help_text="Markdown or HTML content")
    date_posted = models.DateTimeField(auto_now_add=True, db_index=True)
    is_published = models.BooleanField(default=True, db_index=True)

    def save(self, *args, **kwargs):
        is_new_image = False
        if self.image:
            try:
                old_instance = Post.objects.get(pk=self.pk)
                if old_instance.image != self.image:
                    is_new_image = True
            except Post.DoesNotExist:
                is_new_image = True

            if is_new_image:
                img = Image.open(self.image)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
                output = BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)
                file_name = self.image.name.split('.')[0]
                self.image = File(output, name=f"{file_name}.jpg")

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title
