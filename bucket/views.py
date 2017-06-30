from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Bucket, RequestFactory


@csrf_exempt
def add_request(request, bucket_uuid):
    bucket = get_object_or_404(Bucket, pk=bucket_uuid, active=True)
    req = RequestFactory.from_request(request, bucket)

    return HttpResponse('OK', status=req.response_code if req else 400)
