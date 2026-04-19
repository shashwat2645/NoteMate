from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from notes.models import Note
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('email_verified', 'created_at')


class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'date_joined', 'is_verified', 'note_count')
    list_filter = ('is_staff', 'is_superuser', 'date_joined', 'profile__email_verified')
    readonly_fields = ('date_joined', 'last_login')

    def is_verified(self, obj):
        return obj.profile.email_verified if hasattr(obj, 'profile') else False
    is_verified.short_description = 'Verified'
    is_verified.boolean = True

    def note_count(self, obj):
        return obj.notes.count()
    note_count.short_description = 'Notes'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)