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
import sys
from typing import Type, Union
import urllib.parse
import yaml

from osmdi.datafetch import WikibaseFetch
from osmdi.exporter import json_dumper, yaml_dumper


class OsmDI:
    """OpenStreetMap data intent main entrypoint"""

    # initial_ast: None
    # initial_ast_not: None
    # initial_dataitem: None
    # initial_wdata: None

    def __init__(self, osmdi_ast_raw: str, output_format: str = "yaml") -> None:
        osmdi_ast = osmdi_input_parser(osmdi_ast_raw)
        self.output_format = output_format
        self.initial_1 = None
        self.initial_2 = None
        self.initial_ast = None
        self.initial_ast_not = None
        self.initial_dataitem = None
        self.initial_wdata = None

        # if isinstance(osmdi_ast, list):
        #     self.initial_ast = osmdi_ast

        if self._get_from_key(osmdi_ast, 1) is None:
            raise SyntaxError("Invalid input file")

        self.initial_1 = self._get_from_key(osmdi_ast, 1)
        self.initial_2 = self._get_from_key(osmdi_ast, 2)

        self.initial_ast = self._get_from_key(osmdi_ast, 1, 3)
        self.initial_ast_not = self._get_from_key(osmdi_ast, 1, 4)
        self.initial_dataitem = self._get_from_key(osmdi_ast, 1, 5)
        self.initial_wdata = self._get_from_key(osmdi_ast, 1, 10)

    def _get_from_key(
        self, data_block: dict, key: int, subkey: int = None
    ) -> Union[dict, list, str, int]:
        """_summary_

        Args:
            data_block (dict): data to slice
            key (int): key, first level
            subkey (int, optional): key, second level. Defaults to None.

        Returns:
            Union[dict, list, str, int]: the result data
        """
        main = None

        if isinstance(data_block, dict):
            if key in data_block:
                main = data_block[key]
            if str(key) in data_block:
                main = data_block[str(key)]

            if subkey is not None and isinstance(main, dict):
                if subkey in main:
                    return main[subkey]
                if str(key) in data_block:
                    main = data_block[str(key)]
                    return main[str(subkey)]

        return main

    def debug(self):
        # print(self.initial_ast)

        driver_ps = OsmDIDriverPassthrough(self)
        driver_dwl = OsmDIDriverDocWikiLinks(self)
        driver_dti = OsmDIDriverDocTaginfo(self)
        driver_pql = OsmDIDriverPseudoQL(self)
        driver_wdi = OsmDIDriverWikibaseDataItem(self)
        driver_wdata = OsmDIDriverWikibaseWikidata(self)
        driver_wdata_q1 = OsmDIDriverWikibaseWikidata(self).set_mode(1)

        debug_out = {
            # "input": driver_ps.output(),
            # "1": driver_ps.output(),
            1: driver_ps.output(),
            2: self.initial_2, # @TODO make this also consider cli params
            # "output": {
            # "3": {
            3: {
                # "driver": {
                driver_dwl.get_id(): driver_dwl.output(),
                driver_dti.get_id(): driver_dti.output(),
                # driver_oqt.driver_id: driver_oqt.output(),
                driver_pql.get_id(): driver_pql.output(),
                driver_wdi.get_id(): driver_wdi.output(),
                driver_wdata.get_id(): driver_wdata.output(),
                driver_wdata_q1.get_id(): driver_wdata_q1.output(),
                # }
            },
        }

        if self.output_format == "yaml":
            print(yaml_dumper(debug_out))

        elif self.output_format == "json":
            print(json_dumper(debug_out))
        else:
            raise NotImplementedError


class OsmDIDriver(ABC):
    """OsmDIDriver abstract class for all drivers"""

    def __init__(
        self,
        osmdi: Type["OsmDI"],
    ) -> None:
        self.osmdi = osmdi
        # self._driver_id: str = "D0"
        self._driver_id: str = "0"
        self._subcode: int = 0

        # @TODO implement generic error handling at base driver class
        self._errors = []

        self.__post_init__()

    def get_id(self):
        if self._subcode < 1:
            return self._driver_id
        return float(str(self._driver_id) + "." + str(self._subcode))

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
        # self._driver_id = "D3"
        # self._driver_id = "3"
        self._driver_id = 3

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
        # self._driver_id = "D2"
        # self._driver_id = "2"
        self._driver_id = 2
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
        # self._driver_id = "D4"
        # self._driver_id = "4"
        self._driver_id = 4

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
        # self._driver_id = "D1"
        # self._driver_id = "1"
        self._driver_id = 1

    def output(self):
        return self.osmdi.initial_1


class OsmDIDriverPseudoQL(OsmDIDriver):
    """PseudoQL driver"""

    def __post_init__(self):
        # self._driver_id = "D9"
        # self._driver_id = "9"
        self._driver_id = 9
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
        # self._driver_id = "D10"
        # self._driver_id = "10"
        self._driver_id = 10

    def output(self):
        if not self.osmdi.initial_dataitem:
            return None

        wbfetch = WikibaseFetch(self.osmdi.initial_dataitem)
        return wbfetch.get_as_osm_tags()


class OsmDIDriverWikibaseWikidata(OsmDIDriver):
    """Wikibase Wikidata driver"""

    def __post_init__(self):
        # self._driver_id = "D11"
        # self._driver_id = "11"
        self._driver_id = 11

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
    if data_ptr == "-":
        data_str = sys.stdin.read()
        result = yaml.safe_load(data_str)
    else:
        with open(data_ptr, "r") as file:
            result = yaml.safe_load(file)

    return result
