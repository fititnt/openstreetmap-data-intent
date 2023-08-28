#!/bin/sh

osmdi --input-osmdi-compact tests/data/example-002.json | yq -P
osmdi --input-osmdi-compact tests/data/example-003.json | yq -P