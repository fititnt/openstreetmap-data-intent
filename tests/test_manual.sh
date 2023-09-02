#!/bin/sh

osmdi --input-osmdi-compact tests/data/example-002.json | yq -P
osmdi --input-osmdi-compact tests/data/example-003.json | yq -P
yq < tests/data/example-003.json -o props
yq < tests/data/example-004.num.yml -o props

jq -S < tests/data/example-003.json | yq -P

yq -P -I 4 < tests/data/example-004.num.yml
yq -P -I 4 -o props < tests/data/example-004.num.yml