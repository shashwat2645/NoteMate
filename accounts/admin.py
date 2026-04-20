from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.shortcuts import redirect
from notes.models import Note
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('email_verified', 'verification_otp', 'created_at')
    readonly_fields = ('verification_otp', 'created_at')


class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'date_joined', 'is_verified', 'note_count', 'is_admin')
    list_filter = ('is_staff', 'date_joined')
    readonly_fields = ('date_joined', 'last_login')
    list_select_related = ('profile',)
    actions = ['verify_users', 'unverify_users', 'make_admin', 'remove_admin']
    list_per_page = 50

    def is_admin(self, obj):
        return obj.is_staff
    is_admin.short_description = 'Admin'
    is_admin.boolean = True

    def is_verified(self, obj):
        try:
            return obj.profile.email_verified
        except Profile.DoesNotExist:
            return False
    is_verified.short_description = 'Verified'
    is_verified.boolean = True

    def note_count(self, obj):
        return obj.notes.count()
    note_count.short_description = 'Notes'

    def verify_users(self, request, queryset):
        for user in queryset:
            try:
                profile = user.profile
                profile.email_verified = True
                profile.save()
                user.is_active = True
                user.save()
            except Profile.DoesNotExist:
                pass
        self.message_user(request, f'{queryset.count()} users verified.')
    verify_users.short_description = 'Mark selected users as verified'

    def unverify_users(self, request, queryset):
        for user in queryset:
            try:
                profile = user.profile
                profile.email_verified = False
                profile.save()
            except Profile.DoesNotExist:
                pass
        self.message_user(request, f'{queryset.count()} users unverified.')
    unverify_users.short_description = 'Mark selected users as unverified'

    def make_admin(self, request, queryset):
        queryset.update(is_staff=True, is_superuser=True)
        self.message_user(request, f'{queryset.count()} users made admin.')
    make_admin.short_description = 'Make selected users admin'

    def remove_admin(self, request, queryset):
        queryset.update(is_staff=False, is_superuser=False)
        self.message_user(request, f'{queryset.count()} users removed from admin.')
    remove_admin.short_description = 'Remove admin from selected users'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('profile')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        user = self.get_object(request, object_id)
        extra_context = extra_context or {}
        extra_context['show_make_admin'] = user and not user.is_staff
        return super().change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        return super().add_view(request, form_url)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)