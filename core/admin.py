from django.contrib import admin
from django.db.models import Count
from django.utils import timezone
from .models import Profile, Skill, Project, Experience, Certification, Education, ContactMessage

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Experience)
admin.site.register(Certification)
admin.site.register(Education)
admin.site.register(ContactMessage)

