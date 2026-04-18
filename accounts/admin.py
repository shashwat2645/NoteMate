from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from notes.models import Note


class NoteInline(admin.TabularInline):
    model = Note
    extra = 0
    readonly_fields = ('created_at', 'updated_at')
    fields = ('title', 'content', 'created_at', 'updated_at')


class CustomUserAdmin(BaseUserAdmin):
    inlines = (NoteInline,)
    list_display = ('username', 'email', 'date_joined', 'note_count')
    list_filter = ('is_staff', 'is_superuser', 'date_joined')
    readonly_fields = ('date_joined', 'last_login')

    def note_count(self, obj):
        return obj.notes.count()
    note_count.short_description = 'Notes'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)