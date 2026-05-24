from django.contrib import admin
from .models import Profile, Skill, Project, Experience, Certification, Education, ContactMessage

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Experience)
admin.site.register(Certification)
admin.site.register(Education)
admin.site.register(ContactMessage)
