from django.contrib import admin
from django.contrib.admin.helpers import ActionForm
from django.contrib import messages
from django import forms

from .models import Bucket, Request


class BucketAdmin(admin.ModelAdmin):
    readonly_fields = ['url', 'created_at', 'modified_at']
    list_display = ['id', 'title', 'active', 'created_at', 'modified_at']
    list_filter = ['active', 'created_at', 'modified_at']
    search_fields = ['id', 'title', 'description']


class KeyValueForm(ActionForm):
    key = forms.CharField(required=False, max_length=250)
    value = forms.CharField(required=False, max_length=500)


def add_comment(modeladmin, request, queryset):
    comment = request.POST['value']
    for r in queryset.all():
        current_comment = r.comments if r.comments else ''
        r.comments = current_comment + comment
        r.save()


def clear_comment(modeladmin, request, queryset):
    queryset.update(comments="")


def add_key_value(modeladmin, request, queryset):
    key = request.POST['key']
    value = request.POST['value']
    if not key:
        messages.error(request, 'key may not be empty')
        return
    for r in queryset.all():
        if not r.custom_values:
            r.custom_values = {}
        if value:
            r.custom_values[key] = value
        elif key in r.custom_values:
            del r.custom_values[key]
        r.save()


class RequestAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'headers', 'method', 'host', 'remote_address', 'path', 'query_strings', 'body',
                       'response_code', 'http_referer', 'form_data', 'cookies', 'error', 'custom_values', 'created_at',
                       'modified_at']
    list_display = ['id', 'bucket', 'method', 'host', 'remote_address', 'created_at', 'modified_at']
    list_filter = ['method', 'response_code', 'created_at', 'modified_at', 'bucket__title']
    search_fields = ['id', 'headers', 'host', 'remote_address', 'path', 'query_strings', 'body', 'form_data', 'cookies',
                     'error', 'comments']
    ordering = ('-created_at',)
    action_form = KeyValueForm
    actions = [add_comment, clear_comment, add_key_value]


admin.site.register(Bucket, BucketAdmin)
admin.site.register(Request, RequestAdmin)
