from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Recents


class CustomUserAdmin(UserAdmin):

    list_display = ('username', 'email', 'first_name', 'last_name', 'auth_provider', 'profile_picture', 'is_staff', 'is_active')
    list_filter = ('username', 'email', 'first_name', 'last_name', 'auth_provider')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'auth_provider')


class RecentsAdmin(admin.ModelAdmin):

    list_display = ('date_send', 'request', 'trigger')
    list_filter = ('date_send', 'request', 'trigger')
    search_fields = ('date_send', 'request', 'trigger')


admin.site.register(Recents, RecentsAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
