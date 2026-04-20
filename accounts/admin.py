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
    list_display = ('username', 'email', 'date_joined', 'is_verified', 'note_count', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'date_joined')
    readonly_fields = ('date_joined', 'last_login')
    list_select_related = ('profile',)
    actions = ['verify_users', 'unverify_users', 'make_admin', 'remove_admin']

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
        for user in queryset:
            user.is_staff = True
            user.is_superuser = True
            user.save()
        self.message_user(request, f'{queryset.count()} users made admin.')
    make_admin.short_description = 'Make selected users admin'

    def remove_admin(self, request, queryset):
        for user in queryset:
            user.is_staff = False
            user.is_superuser = False
            user.save()
        self.message_user(request, f'{queryset.count()} users removed from admin.')
    remove_admin.short_description = 'Remove admin from selected users'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('profile')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)