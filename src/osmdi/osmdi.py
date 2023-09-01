#!/usr/bin/env python3
# ==============================================================================
#
#          FILE:  osmdi.py
#
#         USAGE:  ---
#
#   DESCRIPTION:  ---
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#       AUTHORS:  Emerson Rocha <rocha[at]ieee.org>
# COLLABORATORS:  ---
#       LICENSE:  Public Domain dedication or Zero-Clause BSD
#                 SPDX-License-Identifier: Unlicense OR 0BSD
#       VERSION:  ---
#       CREATED:  ---
# ==============================================================================
from abc import ABC
import json
from typing import Type
import urllib.parse
import yaml

from osmdi.datafetch import WikibaseFetch


class OsmDI:
    """OpenStreetMap data intent main entrypoint"""

    # initial_ast: None
    # initial_ast_not: None
    # initial_dataitem: None
    # initial_wdata: None

    def __init__(self, osmdi_ast_raw: str) -> None:
        osmdi_ast = osmdi_input_parser(osmdi_ast_raw)
        self.initial_ast = None
        self.initial_ast_not = None
        self.initial_dataitem = None
        self.initial_wdata = None

        if isinstance(osmdi_ast, list):
            self.initial_ast = osmdi_ast

        if isinstance(osmdi_ast, dict) and "osmm" in osmdi_ast:
            self.initial_ast = osmdi_ast["osmm"]

            if "wikidata" in osmdi_ast:
                self.initial_wdata = osmdi_ast["wikidata"]

            if "dataitem" in osmdi_ast:
                self.initial_dataitem = osmdi_ast["dataitem"]

            if "osmm_not" in osmdi_ast:
                self.initial_ast_not = osmdi_ast["osmm_not"]

    def debug(self, as_json: bool = False):
        # print(self.initial_ast)

        driver_ps = OsmDIDriverPassthrough(self)
        driver_dwl = OsmDIDriverDocWikiLinks(self)
        driver_dti = OsmDIDriverDocTaginfo(self)
        driver_pql = OsmDIDriverPseudoQL(self)
        driver_wdi = OsmDIDriverWikibaseDataItem(self)
        driver_wdata = OsmDIDriverWikibaseWikidata(self)
        driver_wdata_q1 = OsmDIDriverWikibaseWikidata(self).set_mode(1)

        debug_out = {
            "input": {"di": driver_ps.output()},
            "output": {
                "driver": {
                    driver_dwl.get_id(): driver_dwl.output(),
                    driver_dti.get_id(): driver_dti.output(),
                    # driver_oqt.driver_id: driver_oqt.output(),
                    driver_pql.get_id(): driver_pql.output(),
                    driver_wdi.get_id(): driver_wdi.output(),
                    driver_wdata.get_id(): driver_wdata.output(),
                    driver_wdata_q1.get_id(): driver_wdata_q1.output(),
                }
            },
        }

        if as_json:
            print(json.dumps(debug_out, ensure_ascii=False, indent=2))
        else:
            print(debug_out)


class OsmDIDriver(ABC):
    """OsmDIDriver abstract class for all drivers"""

    def __init__(
        self,
        osmdi: Type["OsmDI"],
    ) -> None:
        self.osmdi = osmdi
        self._driver_id: str = "D0"
        self._subcode: int = 0

        # @TODO implement generic error handling at base driver class
        self._errors = []

        self.__post_init__()

    def get_id(self):
        if self._subcode < 1:
            return self._driver_id
        return self._driver_id + "." + str(self._subcode)

    def get_option(self, key: str):
        defaults = {"outfmt": "osm"}

        if key in defaults:
            return defaults[key]

        return None

    def set_mode(self, subcode: int = None):
        self._subcode = subcode
        return self


class OsmDIDriverDocTaginfo(OsmDIDriver):
    """DocWikiLinks driver. Output link for wiki documentation

    @TODO implement regional sites https://wiki.openstreetmap.org/wiki/Taginfo/Sites

    The actual URLs may not exist.
    """

    def __post_init__(self):
        self._driver_id = "D3"

        self.osmdi_ast = self.osmdi.initial_ast

    def _get_tagvalues(self):
        tags = set()
        for group in self.osmdi_ast:
            for item in group:
                # @TODO deal with other commands than tags themselves
                tags.add(item)
        return list(tags)

    def output(self):
        out = {}
        for option in self._get_tagvalues():
            out[option] = f"https://taginfo.openstreetmap.org/tags/{option}"

        return out


class OsmDIDriverDocWikiLinks(OsmDIDriver):
    """DocWikiLinks driver. Output link for wiki documentation

    The actual URLs may not exist.
    """

    def __post_init__(self):
        self._driver_id = "D2"
        self.osmdi_ast = self.osmdi.initial_ast

    def _get_tagvalues(self):
        tags = set()
        for group in self.osmdi_ast:
            for item in group:
                # @TODO deal with other commands than tags themselves
                tags.add(item)
        return list(tags)

    def output(self):
        out = {}
        for option in self._get_tagvalues():
            _encoded = urllib.parse.quote(option)
            out[option] = f"https://wiki.openstreetmap.org/wiki/Tag:{_encoded}"
        return out


class OsmDIDriverOverpassQL(OsmDIDriver):
    """OverpassQL driver"""

    def __post_init__(self):
        self._driver_id = "D4"

    def output(self):
        return "TODO OsmDIDriverOverpassQL"
        out = {}
        for option in self._get_tagvalues():
            # _encoded = urllib.parse.quote(option)
            out[option] = f"https://taginfo.openstreetmap.org/tags/{option}"

        return out


class OsmDIDriverOverpassQLTurbo(OsmDIDriver):
    """OverpassQL driver"""

    def __post_init__(self):
        self._driver_id = "D41"
        self.osmdi_ast = self.osmdi.initial_ast

    def _get_query(self) -> str:
        parts = []

        for group in self.osmdi_ast:
            parts.append(self._get_query_block(group))
            # for item in group:
            #     # @TODO deal with other commands than tags themselves
            #     tags.add(item)

        return parts

        query = """
# @TODO OsmDIDriverOverpassQLTurbo
(
  node["crop"="rice"]({{bbox}});
  way["crop"="rice"]({{bbox}});
  relation["crop"="rice"]({{bbox}});
);
out body;
>;
out skel qt;
"""
        return query

    def _get_query_block(self, group: list) -> str:
        # parts =
        # for item in group:

        query = """
# @TODO OsmDIDriverOverpassQLTurbo
(
  node["crop"="rice"]({{bbox}});
  way["crop"="rice"]({{bbox}});
  relation["crop"="rice"]({{bbox}});
);
out body;
>;
out skel qt;
"""
        return query

    def output(self):
        test = self._get_query()

        return test
        out = {}
        for option in self._get_tagvalues():
            # _encoded = urllib.parse.quote(option)
            out[option] = f"https://taginfo.openstreetmap.org/tags/{option}"

        return out


class OsmDIDriverPassthrough(OsmDIDriver):
    """Passthrough driver. Input "pass through" unaltered"""

    def __post_init__(self):
        self._driver_id = "D1"

    def output(self):
        output = {}
        if self.osmdi.initial_ast:
            output["di"] = self.osmdi.initial_ast
        if self.osmdi.initial_ast_not:
            output["di_not"] = self.osmdi.initial_ast_not
        if self.osmdi.initial_dataitem:
            output["di_dataitem"] = self.osmdi.initial_dataitem
        if self.osmdi.initial_wdata:
            output["di_wikidata"] = self.osmdi.initial_wdata

        return output


class OsmDIDriverPseudoQL(OsmDIDriver):
    """PseudoQL driver"""

    def __post_init__(self):
        self._driver_id = "D9"
        self.osmdi_ast = self.osmdi.initial_ast

    def output(self):
        parts = []
        for group in self.osmdi_ast:
            elements = "nwr"
            area = "({{bbox}})"

            group_str = ""
            for item in group:
                key, val = item.split("=")
                group_str += f'["{key}"="{val}"]'

            # parts.append(elements + str(group) + area)
            parts.append(elements + group_str + area)

        templated = "(\n  " + " ;\n  ".join(parts) + " ;" + "\n)->._;"
        return templated


class OsmDIDriverWikibaseDataItem(OsmDIDriver):
    """Wikibase Data Items (OpenStreetMap) driver

    @TODO implement query, at least the Sophox strategy.
          see https://wiki.openstreetmap.org/wiki/Sophox

    """

    def __post_init__(self):
        self._driver_id = "D10"

    def output(self):
        if not self.osmdi.initial_dataitem:
            return None

        wbfetch = WikibaseFetch(self.osmdi.initial_dataitem)
        return wbfetch.get_as_osm_tags()


class OsmDIDriverWikibaseWikidata(OsmDIDriver):
    """Wikibase Wikidata driver"""

    def __post_init__(self):
        self._driver_id = "D11"

    def _get_mode_1(self) -> str:
        items = self.osmdi.initial_wdata
        if len(items) != 1 or items[0][0] != "Q":
            message = f"NotImplementedError for options <[{str( self.osmdi.initial_wdata)}]>  <{items[0][0]}> <{len(items)}>"
            self._errors.append(message)
            return message

        main_item = items[0]
        # main_item = 'lala'

        templated = f"""SELECT DISTINCT ?item ?itemLabel WHERE {{
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }}
  {{
    SELECT DISTINCT ?item WHERE {{
      {{
        ?item p:P31 ?statement0.
        ?statement0 (ps:P31/(wdt:P279*)) wd:{main_item}.
        FILTER(EXISTS {{ ?statement0 prov:wasDerivedFrom ?reference. }})
      }}
    }}
    # LIMIT 100
  }}
}}
"""
        return templated

    def output(self):
        if not self.osmdi.initial_wdata:
            return None

        wbfetch = WikibaseFetch(
            self.osmdi.initial_wdata,
            prefix="wikidata",
            base="https://www.wikidata.org/wiki/Special:EntityData/",
        )

        if self._subcode == 0:
            return wbfetch.get_as_osm_tags()
        if self._subcode == 1:
            return self._get_mode_1()
        raise NotImplementedError


def osmdi_input_parser(data_ptr: str) -> dict:
    with open(data_ptr, "r") as file:
        result = yaml.safe_load(file)

    return result
