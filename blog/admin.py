from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'read_time', 'date_posted', 'is_published')
    list_filter = ('category', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
