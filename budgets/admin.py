from django.contrib import admin
from budgets.models import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'monthly_limit', 'currency', 'is_exceeded')
    list_filter = ('currency', 'created_at')
    search_fields = ('user__username', 'category__name')
    readonly_fields = ('created_at', 'updated_at', 'get_spent_amount', 'get_percentage_used')
    fieldsets = (
        ('User & Category', {
            'fields': ('user', 'category')
        }),
        ('Budget Info', {
            'fields': ('monthly_limit', 'currency')
        }),
        ('Status', {
            'fields': ('get_spent_amount', 'get_percentage_used'), 'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)
        }),
    )

    def is_exceeded(self, obj):
        return obj.is_exceeded
    is_exceeded.boolean = True
    is_exceeded.short_description = 'Budget Exceeded'
