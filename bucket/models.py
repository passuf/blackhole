import json
import uuid
import traceback

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Bucket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(_('Title'), max_length=255)
    description = models.CharField(_('Description'), max_length=255, blank=True, null=True)
    active = models.BooleanField(_('Active'), default=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('Modified at'), auto_now=True)

    def __str__(self):
        return self.title


class Request(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    bucket = models.ForeignKey(Bucket, related_name='requests')
    comments = models.TextField(_('Comments'), blank=True, null=True)
    method = models.CharField(_('Method'), max_length=255, blank=True, null=True)
    headers = models.TextField(_('Headers'), blank=True, null=True)
    remote_address = models.CharField(_('Remote Address'), max_length=255, blank=True, null=True)
    host = models.CharField(_('Host'), max_length=255, blank=True, null=True)
    http_referer = models.CharField(_('HTTP Referer'), max_length=255, blank=True, null=True)
    path = models.CharField(_('Path'), max_length=255, blank=True, null=True)
    query_strings = models.TextField(_('Query Strings'), blank=True, null=True)
    body = models.TextField(_('Body'), blank=True, null=True)
    response_code = models.IntegerField(_('Response Code'), blank=True, null=True)
    form_data = models.TextField('Form Data', blank=True, null=True)
    cookies = models.TextField(_('Cookies'), blank=True, null=True)
    error = models.TextField(_('Error'), blank=True, null=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('Modified at'), auto_now=True)

    def __str__(self):
        if self.method and self.path:
            return '{method} {path}'.format(method=self.method, path=self.path)
        return str(self.created_at)


class RequestFactory:
    @staticmethod
    def from_request(request, bucket):
        req = Request.objects.create(
            bucket=bucket,
            path=request.path,
            method=request.method,
            host=request.get_host(),
            response_code=200,
        )

        errors = ''

        # Parse the HEADER
        try:
            # Find non-serializable keys
            keys_to_remove = []
            for key in request.META.keys():
                # Remove WSGI related keys
                if key.startswith('wsgi.'):
                    keys_to_remove.append(key)
                    continue

                # Try if object is serializable
                try:
                    json.dumps(request.META[key])
                except Exception:
                    keys_to_remove.append(key)
                    continue

            # Remove invalid keys
            for key in keys_to_remove:
                request.META.pop(key, None)

            # Finally try to parse the header
            req.headers = json.dumps(request.META)
        except Exception as e:
            print(e, traceback.format_exc())
            req.headers = request.META
            errors += '\n' + str(traceback.format_exc())

        # Parse the remote address
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                req.remote_address = x_forwarded_for.split(',')[0]
            else:
                req.remote_address = request.META.get('REMOTE_ADDR')
        except Exception as e:
            print(e, traceback.format_exc())
            req.remote_address = 'error'
            errors += '\n' + str(traceback.format_exc())

        # Parse the HTTP Referer
        try:
            req.http_referer = request.META.get('HTTP_REFERER')
        except Exception as e:
            print(e, traceback.format_exc())
            req.http_referer = 'error'
            errors += '\n' + str(traceback.format_exc())

        # Parse the body
        try:
            req.body = json.dumps(request.body.decode('utf-8'))
        except Exception as e:
            print(e, traceback.format_exc())
            req.body = 'error'
            errors += '\n' + str(traceback.format_exc())

        # Parse GET params
        try:
            req.query_strings = json.dumps(request.GET)
        except Exception as e:
            print(e, traceback.format_exc())
            req.query_strings = 'error'
            errors += '\n' + str(traceback.format_exc())

        # Parse POST params
        try:
            req.form_data = json.dumps(request.POST)
        except Exception as e:
            print(e, traceback.format_exc())
            req.form_data = 'error'
            errors += '\n' + str(traceback.format_exc())

        # Parse Cookies
        try:
            req.cookies = json.dumps(request.COOKIES)
        except Exception as e:
            print(e, traceback.format_exc())
            req.cookies = 'error'
            errors += '\n' + str(traceback.format_exc())

        if errors:
            req.error = errors
            req.response_code = 400

        # Save the request
        req.save()

        return req

