from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property


@cache_page(60 * 15, key_prefix='property_list')
def property_list(request):
    if request.method == 'GET':
        properties = Property.objects.all()
        data = {'properties': list(properties.values())}
        return JsonResponse(data=data, status=200, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)