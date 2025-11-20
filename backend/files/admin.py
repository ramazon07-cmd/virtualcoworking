from django.contrib import admin
from .models import File, Note


class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_by', 'team', 'created_at')
    list_filter = ('team', 'created_at')
    search_fields = ('name', 'uploaded_by__username')
    date_hierarchy = 'created_at'


class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'team', 'created_at', 'updated_at')
    list_filter = ('team', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'


admin.site.register(File, FileAdmin)
admin.site.register(Note, NoteAdmin)
