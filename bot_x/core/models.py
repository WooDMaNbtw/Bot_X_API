from django.db import models


class Log(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    """PROXY FIELDS"""
    proxy_method = models.CharField(max_length=10, null=True, blank=True)
    proxy_url = models.URLField(max_length=255, null=True, blank=True)
    proxy_request_headers = models.JSONField(null=True, blank=True)
    proxy_request_body = models.JSONField(null=True, blank=True)
    proxy_response_headers = models.JSONField(null=True, blank=True)
    proxy_response_body = models.JSONField(null=True, blank=True)
    proxy_response_status_code = models.PositiveIntegerField(null=True, blank=True)

    '''CORE FIELDS'''
    core_method = models.CharField(max_length=10, null=True, blank=True)
    core_url = models.URLField(max_length=255, null=True, blank=True)
    core_request_headers = models.JSONField(null=True, blank=True)
    core_request_body = models.JSONField(null=True, blank=True)
    core_response_headers = models.JSONField(null=True, blank=True)
    core_response_body = models.JSONField(null=True, blank=True)
    core_response_status_code = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Created at - {self.created_at} | Proxy method - {self.proxy_method} | Core method - {self.core_method}"

    class Meta:
        ordering = ["id"]
        verbose_name = "Log"
        verbose_name_plural = "Logs"