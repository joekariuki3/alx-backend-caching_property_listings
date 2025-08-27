from django.urls import path
from .views import property_list, cache_metrics

urlpatterns = [
    path('', property_list, name='property_list'),
    path('cache_metrics/', cache_metrics, name='cache_metrics')
]