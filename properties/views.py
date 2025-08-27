from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property
from .utils import get_all_properties, get_redis_cache_metrics


@cache_page(60 * 15)
def property_list(request):
    if request.method == 'GET':
        properties = get_all_properties()
        data = {'properties': list(properties.values())}
        return JsonResponse(data=data, status=200, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def cache_metrics(request):
    if request.method == 'GET':
        metrics = get_redis_cache_metrics()
        return JsonResponse(data=metrics, status=200)