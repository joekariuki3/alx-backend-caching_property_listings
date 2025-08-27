from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
from logging import getLogger

def get_all_properties():
    """
    Retrieve all Property objects from the database or cache.

    This function checks if a cached queryset exists. If it does, the cached
    queryset is returned. Otherwise, it queries the database to get all Property
    objects, caches the result for a duration, and returns the queryset.

    Returns:
        QuerySet: The queryset of all Property objects.

    Raises:
        None
    """
    queryset = cache.get('all_properties')
    if queryset is None:
        queryset = Property.objects.all()
        cache.set('all_properties', queryset, 3600)
    return queryset

def get_redis_cache_metrics():
    """
    Fetches and calculates Redis cache performance metrics, including hits, misses,
    and hit ratio. This function retrieves data from a specified Redis connection
    and organizes the metrics into a dictionary for performance analysis.

    Returns
    -------
    dict
        A dictionary containing Redis cache performance metrics. The keys include:
        - hits: Number of successful cache hits.
        - misses: Number of cache misses.
        - hit_ratio: Ratio of hits to total cache accesses. (hits / (hits + misses)).
        In case of an exception, the dictionary will contain an 'error' key
        with the error message as its value.
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
        logger = getLogger(__name__)
        logger.error(f"Error: {e}")
        return {'error': str(e)}