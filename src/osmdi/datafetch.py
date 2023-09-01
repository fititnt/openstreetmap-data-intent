# @see https://requests-cache.readthedocs.io/en/stable/

import json
from typing import Union
from .constants import CACHE_TTL, CACHE_DBNAME, CACHE_DRIVER


class DataFetch:
    def __init__(self, use_cache: bool = True) -> None:
        self.use_cache = use_cache

    def debug(self):
        import requests_cache

        session = requests_cache.CachedSession(
            CACHE_DBNAME,
            backend=CACHE_DRIVER,
            expire_after=CACHE_TTL,
            allowable_codes=[200, 400, 404, 500],
            stale_if_error=True,
        )
        for i in range(60):
            print(session.get("https://httpbin.org/delay/1"))

    def get_url(self, url: str):
        if self.use_cache:
            import requests_cache

            session = requests_cache.CachedSession(
                CACHE_DBNAME,
                backend=CACHE_DRIVER,
                expire_after=CACHE_TTL,
                allowable_codes=[200, 400, 404, 500],
                stale_if_error=True,
            )

            return session.get(url)
        else:
            raise NotImplementedError("TODO implement without requests-cache")


# Q16917
# https://www.wikidata.org/wiki/Special:EntityData/Q16917.json

# Q4941 on Data Items | amenity=hospital (Q4941)
# https://wiki.openstreetmap.org/wiki/Special:EntityData/Q4941.json


# def wikibase_to_osmtags(wikibase_resp: str, ids: Union[str, list]):
def wikibase_to_osmtags(wikibase_resp: str, ids: list, wikibase_prefix: str = "osmi"):
    items = []
    try:
        resp = json.loads(wikibase_resp)
        for id in ids:
            item = []
            resp["entities"][id]
            item.append(f"#{wikibase_prefix}={id}")
    except:
        return ["#wikibase_to_osmtags err"]

    return items
