from django.contrib import admin
from accounts.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_currency', 'created_at')
    list_filter = ('preferred_currency', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Profile', {
            'fields': ('avatar', 'bio', 'preferred_currency')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)
        }),
    )
