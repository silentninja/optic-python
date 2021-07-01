from django.db import connection
from django.http import HttpResponse, JsonResponse


def view1(request):
    return HttpResponse('view1')


def view2(request):
    return HttpResponse('view2')


def json_view(request):
    return JsonResponse({'foo': 'bar'})
