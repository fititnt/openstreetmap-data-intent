#!/bin/sh

osmdicli tests/data/example-002.json | yq -P
osmdicli tests/data/example-003.json | yq -P
yq < tests/data/example-003.json -o props
yq < tests/data/example-004.num.yml -o props

jq -S < tests/data/example-003.json | yq -P

yq -P -I 4 < tests/data/example-004.num.yml
yq -P -I 4 -o props < tests/data/example-004.num.yml

osmdicli tests/data/example-005.osmdi.yml

# shellcheck disable=SC2002
cat tests/data/example-003.json | osmdicli -O yaml - | yq
# shellcheck disable=SC2002
cat tests/data/example-003.json | osmdicli -O yaml - | yq