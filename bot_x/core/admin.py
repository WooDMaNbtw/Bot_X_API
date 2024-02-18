from django.contrib import admin
from .models import Log


@admin.register(Log)
class Log(admin.ModelAdmin):
    list_display = [field.name for field in Log._meta.get_fields()]
    list_filter = ("created_at", "core_response_status_code")
    search_fields = ('core_response_status_code', "proxy_response_body", 'core_response_body')