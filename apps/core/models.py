from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Profile(models.Model):
    """Single profile record - only one instance allowed"""
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    tagline = models.TextField()
    about = models.TextField()
    profile_image = models.ImageField(upload_to='profile/')
    logo = models.ImageField(upload_to='logo/')
    resume_file = models.FileField(upload_to='resume/')
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text='Optional phone number')
    github_url = models.URLField()
    linkedin_url = models.URLField()
    twitter_url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.pk = 1  # Enforce single record
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"


class Skill(models.Model):
    """Skills grouped by category"""
    CATEGORY_CHOICES = [
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Database', 'Database'),
        ('Data', 'Data'),
        ('Tools', 'Tools'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=100, blank=True, help_text='Icon class name (optional)')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['category', 'order']

    def __str__(self):
        return f"{self.name} ({self.category})"


class Project(models.Model):
    """Portfolio projects"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=250, blank=True)
    description = models.TextField()
    tech_stack = models.CharField(max_length=500, help_text='Comma-separated technologies')
    github_link = models.URLField()
    live_link = models.URLField(blank=True, null=True, help_text='Optional live demo URL')
    image = models.ImageField(upload_to='projects/')
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-is_featured']

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Certificate(models.Model):
    """Professional certificates"""
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    date = models.DateField()
    certificate_image = models.ImageField(upload_to='certificates/')
    certificate_link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} - {self.issuer}"


class Experience(models.Model):
    """Work experience"""
    company_name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text='Leave blank for current position')
    description = models.TextField(help_text='Use HTML for bullet points')
    location = models.CharField(max_length=200, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-start_date']

    def __str__(self):
        return f"{self.role} at {self.company_name}"

    @property
    def is_current(self):
        return self.end_date is None

    @property
    def duration(self):
        end = self.end_date or timezone.now().date()
        years = (end - self.start_date).days // 365
        months = ((end - self.start_date).days % 365) // 30
        if years > 0 and months > 0:
            return f"{years} yr{ 's' if years > 1 else ''} {months} mo{ 's' if months > 1 else ''}"
        elif years > 0:
            return f"{years} yr{ 's' if years > 1 else ''}"
        else:
            return f"{months} mo{ 's' if months > 1 else ''}"


class Achievement(models.Model):
    """Achievements and awards"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(null=True, blank=True)
    icon = models.CharField(max_length=100, blank=True, help_text='Icon class or emoji')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-date']

    def __str__(self):
        return self.title
