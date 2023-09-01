

# @see https://requests-cache.readthedocs.io/en/stable/

from .constants import (
    CACHE_TTL,
    CACHE_DBNAME
)



class DataFetch:
    def debug(self):
        import requests_cache
        session = requests_cache.CachedSession(CACHE_DBNAME)
        for i in range(60):
            print(session.get('https://httpbin.org/delay/1'))