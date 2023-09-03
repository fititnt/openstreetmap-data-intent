# @see https://requests-cache.readthedocs.io/en/stable/

import json
from typing import List, Union

from .util import osmdi_langs_preferred
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

            return session.get(url).text
        else:
            raise NotImplementedError("TODO implement without requests-cache")


class WikibaseFetch:
    def __init__(
        self,
        items: list,
        prefix="osmi",
        base: str = "https://wiki.openstreetmap.org/wiki/Special:EntityData/",
    ) -> None:
        self.items = items
        self.prefix = prefix
        self.base = base
        self._lang_preferences: list = None
        self._result = None

    def prepare(self):
        if self._result is None:
            self._result = []

            apiresp = DataFetch()

            for id in self.items:
                _url = self.base + id + ".json"
                respnow = apiresp.get_url(_url)
                parsed = wikibase_to_osmtags(
                    respnow, [id], self._lang_preferences, wikibase_prefix=self.prefix
                )
                self._result.extend(parsed)
                # self._result.append(respnow)

            # self._result = apiresp.get_url()

    def get_as_osm_tags(self):
        self.prepare()
        # result = ["@TODO"]
        # return result
        return self._result

    def set_language_preferences(self, preferences: List[list] = None):
        self._lang_preferences = preferences
        return self


# Q16917
# https://www.wikidata.org/wiki/Special:EntityData/Q16917.json

# Q4941 on Data Items | amenity=hospital (Q4941)
# https://wiki.openstreetmap.org/wiki/Special:EntityData/Q4941.json


# def wikibase_to_osmtags(wikibase_resp: str, ids: Union[str, list]):
def wikibase_to_osmtags(
    wikibase_resp: str,
    ids: list,
    lang_preferences: List[list] = None,
    wikibase_prefix: str = "osmi",
):
    items = []
    try:
        resp = json.loads(wikibase_resp)
        for id in ids:
            item = []
            active = resp["entities"][id]
            item.append(f"ref={wikibase_prefix}{id}")

            if "aliases" in active and isinstance(active["aliases"], dict):

                lang_aliases_filtered = osmdi_langs_preferred(
                    active["aliases"].keys(),
                    lang_preferences
                )
                # for lang in active["aliases"]:
                for lang in lang_aliases_filtered:
                    if isinstance(active["aliases"][lang], str):
                        item.append(
                            f"alt_name:{lang}={active['aliases'][lang]['value']}"
                        )
                    else:
                        value_list = []
                        for _i in active["aliases"][lang]:
                            value_list.append(_i["value"])
                        result = "␞".join(value_list)
                        result_scaped = result.replace(";", ";;")
                        # final_value = result_scaped.replace(0xE2, ";")
                        final_value = result_scaped.replace("␞", ";")
                        item.append(f"alt_name:{lang}={final_value}")

            if "descriptions" in active:
                lang_desc_filtered = osmdi_langs_preferred(
                    active["descriptions"].keys(),
                    lang_preferences
                )                
                # for lang in active["descriptions"]:
                for lang in lang_desc_filtered:
                    item.append(
                        f"description:{lang}={active['descriptions'][lang]['value']}"
                    )

            if "labels" in active:

                lang_labels_filtered = osmdi_langs_preferred(
                    active["labels"].keys(),
                    lang_preferences
                )      

                # for lang in active["labels"]:
                for lang in lang_labels_filtered:
                    item.append(f"name:{lang}={active['labels'][lang]['value']}")

            item.sort()
            items.append(item)

    except Exception as err:
        return ["#wikibase_to_osmtags err", str(err)]

    return items
