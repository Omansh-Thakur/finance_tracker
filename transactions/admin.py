from django.contrib import admin
from transactions.models import Category, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'type', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'name', 'type')
        }),
        ('Details', {
            'fields': ('description',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)
        }),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'category', 'amount', 'currency', 'user')
    list_filter = ('currency', 'date', 'category__type')
    search_fields = ('description', 'user__username', 'category__name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User & Category', {
            'fields': ('user', 'category')
        }),
        ('Transaction Details', {
            'fields': ('amount', 'currency', 'date', 'description')
        }),
        ('Receipt', {
            'fields': ('receipt',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)
        }),
    )
