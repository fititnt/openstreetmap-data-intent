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
import urllib.parse
import yaml


class OsmDI:
    """OpenStreetMap data intent main entrypoint"""

    initial_ast: None
    initial_ast_not: None
    initial_dataitem: None
    initial_wdata: None

    def __init__(self, osmdi_ast_raw: str) -> None:
        osmdi_ast = osmdi_input_parser(osmdi_ast_raw)
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

        driver_ps = OsmDIDriverPassthrough(self.initial_ast)
        driver_dwl = OsmDIDriverDocWikiLinks(self.initial_ast)
        driver_dti = OsmDIDriverDocTaginfo(self.initial_ast)
        # driver_oqt = OsmDIDriverOverpassQLTurbo(self.initial_ast)
        driver_pql = OsmDIDriverPseudoQL(self.initial_ast)
        driver_wdi = OsmDIDriverWikibaseDataItem(self.initial_ast)

        debug_out = {
            "input": {"di": driver_ps.output()},
            "output": {
                "driver": {
                    driver_dwl.driver_id: driver_dwl.output(),
                    driver_dti.driver_id: driver_dti.output(),
                    # driver_oqt.driver_id: driver_oqt.output(),
                    driver_pql.driver_id: driver_pql.output(),
                }
            },
        }

        if self.initial_dataitem:
            debug_out["input"]["di_dataitem"] = self.initial_dataitem

        if self.initial_wdata:
            debug_out["input"]["di_wikidata"] = self.initial_wdata

        # debug_out.

        # print(driver_ps.output())
        # print(driver_ps)

        if as_json:
            print(json.dumps(debug_out, ensure_ascii=False, indent=2))
        else:
            print(debug_out)


class OsmDIDriver(ABC):
    """OsmDIDriver abstract class for all drivers"""

    def __init__(
        self,
        osmdi_ast: list = None,
        osmdi_not: list = None,
        dataitem: list = None,
        wikidata: list = None,
    ) -> None:
        self.osmdi_ast = osmdi_ast
        self.osmdi_not = osmdi_not
        self.dataitem = dataitem
        self.wikidata = wikidata
        self.driver_id = "D0"

        self.__post_init__()

    def get_option(self, key: str):
        defaults = {"outfmt": "osm"}

        if key in defaults:
            return defaults[key]

        return None


class OsmDIDriverDocTaginfo(OsmDIDriver):
    """DocWikiLinks driver. Output link for wiki documentation

    @TODO implement regional sites https://wiki.openstreetmap.org/wiki/Taginfo/Sites

    The actual URLs may not exist.
    """

    def __post_init__(self):
        self.driver_id = "D3"

    def _get_tagvalues(self):
        tags = set()
        for group in self.osmdi_ast:
            for item in group:
                # @TODO deal with other commands than tags themselves
                tags.add(item)
        return list(tags)

    def output(self):
        # return self.osmdi_ast
        # return "todo"

        out = {}
        for option in self._get_tagvalues():
            # _encoded = urllib.parse.quote(option)
            out[option] = f"https://taginfo.openstreetmap.org/tags/{option}"

        return out


class OsmDIDriverDocWikiLinks(OsmDIDriver):
    """DocWikiLinks driver. Output link for wiki documentation

    The actual URLs may not exist.
    """

    def __post_init__(self):
        self.driver_id = "D2"

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
        self.driver_id = "D4"

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
        self.driver_id = "D41"

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
        self.driver_id = "D1"

    def output(self):
        return self.osmdi_ast


class OsmDIDriverPseudoQL(OsmDIDriver):
    """PseudoQL driver"""

    def __post_init__(self):
        self.driver_id = "D9"

    def output(self):
        # return "TODO OsmDIDriverPseudoQL"

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
            # for item in group:
            #     parts.

        # _rules = " ;\n  ".join(parts) + ';'

        templated = "(\n  " + " ;\n  ".join(parts) + " ;" + "\n)->._;"

        # return  " + ".join(parts) + ';'
        # return  " ; ".join(parts) + ';'
        return templated


class OsmDIDriverWikibaseDataItem(OsmDIDriver):
    """Wikibase Data Items (OpenStreetMap) driver"""

    def __post_init__(self):
        self.driver_id = "D10"

    def output(self):
        # return "TODO OsmDIDriverPseudoQL"

        if not self.initial_dataitem:
            return None

        # TODO fetch the data
        return self.initial_dataitem


def osmdi_input_parser(data_ptr: str) -> dict:
    with open(data_ptr, "r") as file:
        result = yaml.safe_load(file)

    return result
