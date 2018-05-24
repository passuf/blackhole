from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<bucket_uuid>[0-9a-f-]+)/$', views.add_request, name='add_request'),
    url(r'^(?P<bucket_uuid>[0-9a-f-]+)/show$', views.show_requests, name='add_request'),
]
