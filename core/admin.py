from django.contrib import admin
from django.db.models import Count
from django.utils import timezone
from .models import Profile, Skill, Project, Experience, Certification, Education, ContactMessage, VisitorLog

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Experience)
admin.site.register(Certification)
admin.site.register(Education)
admin.site.register(ContactMessage)

@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ('path', 'ip_address', 'method', 'timestamp')
    list_filter = ('method', 'timestamp')
    search_fields = ('path', 'ip_address', 'user_agent')
    readonly_fields = [f.name for f in VisitorLog._meta.fields]
    
    change_list_template = "admin/core/visitorlog/change_list.html"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        extra_context['total_visitors'] = VisitorLog.objects.count()
        extra_context['today_visitors'] = VisitorLog.objects.filter(timestamp__gte=today).count()
        
        top_paths = VisitorLog.objects.values('path').annotate(count=Count('path')).order_by('-count')[:5]
        extra_context['top_paths'] = top_paths
        
        return super().changelist_view(request, extra_context=extra_context)
