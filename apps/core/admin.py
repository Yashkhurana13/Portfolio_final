from django.contrib import admin
from .models import Profile, Skill, Project, Certificate, Experience, Achievement


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email')
    readonly_fields = ('id',)

    def has_add_permission(self, request):
        # Only allow one profile
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('category', 'order')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'order')
    list_filter = ('is_featured',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order', '-is_featured')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuer', 'date')
    list_filter = ('date',)
    search_fields = ('title', 'issuer')
    ordering = ('-date',)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company_name', 'start_date', 'end_date', 'order')
    list_filter = ('company_name',)
    search_fields = ('role', 'company_name', 'description')
    ordering = ('order', '-start_date')


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'order')
    list_filter = ('date',)
    search_fields = ('title', 'description')
    ordering = ('order', '-date')
