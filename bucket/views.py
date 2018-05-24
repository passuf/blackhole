import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Bucket, RequestFactory


@csrf_exempt
def add_request(request, bucket_uuid):
    bucket = get_object_or_404(Bucket, pk=bucket_uuid, active=True)
    req = RequestFactory.from_request(request, bucket)

    return HttpResponse('OK', status=req.response_code if req else 400)


@login_required
def show_requests(request, bucket_uuid):
    bucket = get_object_or_404(Bucket, pk=bucket_uuid, active=True)
    requests = []
    for r in bucket.requests.all():
        try:
            form_data = json.loads(r.form_data)
            if form_data:
                requests.append(form_data)
        except Exception:
            pass
    return render(request, 'bucket/show.html', {'bucket': bucket, 'requests': requests})
