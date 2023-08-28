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

    def __init__(self, osmdi_ast_raw: str) -> None:
        osmdi_ast = osmdi_input_parser(osmdi_ast_raw)
        self.initial_ast = osmdi_ast
        pass

    def debug(self, as_json: bool = False):
        # print(self.initial_ast)

        driver_ps = OsmDIDriverPassthrough(self.initial_ast)
        driver_dwl = OsmDIDriverDocWikiLinks(self.initial_ast)
        driver_dti = OsmDIDriverDocTaginfo(self.initial_ast)
        driver_oqt = OsmDIDriverOverpassQLTurbo(self.initial_ast)

        debug_out = {
            "input": {"di": driver_ps.output()},
            "output": {
                "driver": {
                    driver_dwl.driver_id: driver_dwl.output(),
                    driver_dti.driver_id: driver_dti.output(),
                    driver_oqt.driver_id: driver_oqt.output(),
                }
            },
        }

        # debug_out.

        # print(driver_ps.output())
        # print(driver_ps)

        if as_json:
            print(json.dumps(debug_out, ensure_ascii=False, indent=2))
        else:
            print(debug_out)


class OsmDIDriver(ABC):
    """OsmDIDriver abstract class for all drivers"""

    def __init__(self, osmdi_ast: str) -> None:
        self.osmdi_ast = osmdi_ast
        self.driver_id = "D0"

        self.__post_init__()


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

    def output(self):

        test = """
(
  node["crop"="rice"]({{bbox}});
  way["crop"="rice"]({{bbox}});
  relation["crop"="rice"]({{bbox}});
);
out body;
>;
out skel qt;
"""

        return "TODO OsmDIDriverOverpassQLTurbo"  + test
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


def osmdi_input_parser(data_ptr: str) -> dict:
    with open(data_ptr, "r") as file:
        result = yaml.safe_load(file)

    return result
