from django.contrib import admin
from .models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu_name', 'parent', 'order', 'resolved_url_display')
    list_filter = ('menu_name',)
    search_fields = ('title', 'explicit_url', 'named_url')
    ordering = ('menu_name', 'parent__id', 'order')

    def resolved_url_display(self, obj):
        return obj.resolved_url or '-'

    resolved_url_display.short_description = 'URL'
