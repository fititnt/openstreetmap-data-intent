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
import yaml


class OsmDI:
    """OpenStreetMap data intent main entrypoint"""

    initial_ast: None

    def __init__(self, osmdi_ast_raw: str) -> None:
        osmdi_ast = osmdi_input_parser(osmdi_ast_raw)
        self.initial_ast = osmdi_ast
        pass

    def debug(self):
        print(self.initial_ast)

        driver_ps = OsmDIDriverPassthrough(self.initial_ast)

        print(driver_ps.output())


class OsmDIDriver(ABC):
    """OsmDIDriver abstract class for all drivers"""

    def __init__(self, osmdi_ast: str) -> None:
        self.osmdi_ast = osmdi_ast


class OsmDIDriverPassthrough(OsmDIDriver):
    """Passthrough driver. Input "pass through" unaltered"""

    def output(self):
        return self.osmdi_ast


def osmdi_input_parser(data_ptr: str) -> dict:
    with open(data_ptr, "r") as file:
        result = yaml.safe_load(file)

    return result
