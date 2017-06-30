from django.contrib import admin

from .models import Bucket, Request


class BucketAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'modified_at']
    list_display = ['id', 'title', 'active', 'created_at', 'modified_at']
    list_filter = ['active', 'created_at', 'modified_at']
    search_fields = ['id', 'title', 'description']


class RequestAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'headers', 'method', 'host', 'remote_address', 'path', 'query_strings', 'body',
                       'response_code', 'http_referer', 'form_data', 'cookies', 'error', 'created_at', 'modified_at']
    list_display = ['id', 'bucket', 'method', 'host', 'remote_address', 'created_at', 'modified_at']
    list_filter = ['method', 'response_code', 'created_at', 'modified_at', 'bucket__title']
    search_fields = ['id', 'headers', 'host', 'remote_address', 'path', 'query_strings', 'body', 'form_data', 'cookies',
                     'error', 'comments']

    ordering = ('-created_at',)

admin.site.register(Bucket, BucketAdmin)
admin.site.register(Request, RequestAdmin)
