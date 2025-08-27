from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection

def get_all_properties():
    """
    Fetches all properties, retrieving them from the cache if available, or from the
    database if not cached, and stores the query result in cache for future calls.

    Returns:
        QuerySet: A queryset containing all Property objects.
    """
    queryset = cache.get('all_properties')
    if queryset is None:
        queryset = Property.objects.all()
        cache.set('all_properties', queryset, 3600)
    return queryset

def get_redis_cache_metrics():
    """
    Retrieve and calculate Redis cache metrics.

    This function connects to a Redis database using a default connection, retrieves
    cache information, calculates key performance metrics (keyspace hits, keyspace
    misses, and hit ratio), and then returns these metrics as a dictionary.

    Returns
    -------
    dict
        A dictionary containing:
            - hits: int
                The number of successful key lookups in the Redis cache.
            - misses: int
                The number of unsuccessful key lookups in the Redis cache.
            - hit_ratio: float
                The ratio of cache hits to total cache lookups.
    """
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()
        hits = info['keyspace_hits']
        misses = info['keyspace_misses']
        hit_ratio = hits / (hits + misses)
        metrics = {
            'hits': hits,
            'misses': misses,
            'hit_ratio': hit_ratio
        }
        return metrics
    except Exception as e:
        return {'error': str(e)}