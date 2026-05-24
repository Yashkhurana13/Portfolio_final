from django.db import models
from django.core.validators import FileExtensionValidator

class Profile(models.Model):
    name = models.CharField(max_length=100)
    about_text = models.TextField()
    is_available = models.BooleanField(default=True)
    available_badge_text = models.CharField(max_length=100, default="Available for opportunities")
    typewriter_words = models.CharField(max_length=500, default="Student,Web Developer,Data Analyst", help_text="Comma separated words")
    about_terminal_lines = models.TextField(help_text="Lines for the about terminal animation, separated by newlines.", default="> whoami\\nSoftware Developer\\n> status\\nBuilding awesome things\\n> _")
    resume = models.FileField(
        upload_to='resumes/', blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Upload a PDF resume only"
    )
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    leetcode_link = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True, help_text="Contact email shown in Contact & Footer")
    card_1_title = models.CharField(max_length=100, default="Currently Learning")
    card_1_text = models.CharField(max_length=200, default="Django, React, & System Design")
    card_2_title = models.CharField(max_length=100, default="Working On")
    card_2_text = models.CharField(max_length=200, default="Premium Agentic Portfolio App")
    card_3_title = models.CharField(max_length=100, default="Focused On")
    card_3_text = models.CharField(max_length=200, default="High Performance Web Architectures")

    def __str__(self):
        return self.name

    @property
    def leetcode_username(self):
        if self.leetcode_link:
            parts = [p for p in self.leetcode_link.strip('/').split('/') if p]
            if parts:
                return parts[-1]
        return None


class Skill(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, help_text="e.g., Language, Framework")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.category})"

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(
        upload_to='projects/', blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])]
    )
    tags = models.CharField(max_length=200, help_text="Comma-separated tags e.g., Django, Python, JS")
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

from tinymce.models import HTMLField

class Experience(models.Model):
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=False)
    description = HTMLField()

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.role} at {self.company}"

class Certification(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    date_issued = models.DateField()
    link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-date_issued']

    def __str__(self):
        return self.title

class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=False)
    grade = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., GPA, Percentage, or CGPA")
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} at {self.institution}"



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_sent']

    def __str__(self):
        return f"Message from {self.name} on {self.date_sent.strftime('%Y-%m-%d')}"
