from django.contrib import admin
from django.contrib.admin.helpers import ActionForm
from django import forms

from .models import Bucket, Request


class BucketAdmin(admin.ModelAdmin):
    readonly_fields = ['url', 'created_at', 'modified_at']
    list_display = ['id', 'title', 'active', 'created_at', 'modified_at']
    list_filter = ['active', 'created_at', 'modified_at']
    search_fields = ['id', 'title', 'description']


class AddCommentForm(ActionForm):
    comment = forms.CharField(required=False, max_length=500)


def add_comment(modeladmin, request, queryset):
    comment = request.POST['comment']
    for r in queryset.all():
        current_comment = r.comments if r.comments else ''
        r.comments = current_comment + comment
        r.save()


def clear_comment(modeladmin, request, queryset):
    queryset.update(comments="")


class RequestAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'headers', 'method', 'host', 'remote_address', 'path', 'query_strings', 'body',
                       'response_code', 'http_referer', 'form_data', 'cookies', 'error', 'created_at', 'modified_at']
    list_display = ['id', 'bucket', 'method', 'host', 'remote_address', 'created_at', 'modified_at']
    list_filter = ['method', 'response_code', 'created_at', 'modified_at', 'bucket__title']
    search_fields = ['id', 'headers', 'host', 'remote_address', 'path', 'query_strings', 'body', 'form_data', 'cookies',
                     'error', 'comments']
    ordering = ('-created_at',)
    action_form = AddCommentForm
    actions = [add_comment, clear_comment]

admin.site.register(Bucket, BucketAdmin)
admin.site.register(Request, RequestAdmin)
