# openstreetmap-data-intent, proof of concept
[early-draft] See https://docs.google.com/presentation/d/1V3gDPh5uzmIYtuPptFJY1GbfbvnxW_ViWuIsnSr9bhQ/edit?usp=sharing

<!-- TOC depthfrom:2 orderedlist:false -->

- [Installing](#installing)
- [Command line Usage](#command-line-usage)
    - [Quickstart](#quickstart)
- [The proto specification for OSM data intent file](#the-proto-specification-for-osm-data-intent-file)
    - [Reference codes at top level](#reference-codes-at-top-level)
    - [1: input data](#1-input-data)
        - [1.1: natural language expalantion, from developer to developer](#11-natural-language-expalantion-from-developer-to-developer)
        - [1.2: natural language example of averange user query](#12-natural-language-example-of-averange-user-query)
        - [1.3: OpenStreetMap tags for select data](#13-openstreetmap-tags-for-select-data)
        - [1.4: OpenStreetMap tags for exclude data](#14-openstreetmap-tags-for-exclude-data)
        - [1.5: OpenStreetMap Wikibase Data Item](#15-openstreetmap-wikibase-data-item)
        - [1.10: Wikidata Wikibase Q items](#110-wikidata-wikibase-q-items)
        - [1.20: operation inside place](#120-operation-inside-place)
            - [1.20.1: operation inside place, parameter natural language](#1201-operation-inside-place-parameter-natural-language)
            - [1.20.2: operation inside place, parameter OSM tagging](#1202-operation-inside-place-parameter-osm-tagging)
            - [1.20.3: operation inside place, parameter OSM relation](#1203-operation-inside-place-parameter-osm-relation)
            - [1.20.4: operation inside place, parameter Wikidata concept](#1204-operation-inside-place-parameter-wikidata-concept)
    - [2: environment data](#2-environment-data)
        - [2.1 prefered natural languages to restrict output if too many options](#21-prefered-natural-languages-to-restrict-output-if-too-many-options)
    - [3: output data](#3-output-data)

<!-- /TOC -->


## Installing

```bash
# pip install osmdi --upgrade
pip install git+https://github.com/fititnt/openstreetmap-data-intent.git#egg=osmdi
```


<!--
### Environment variables
Customize for your needs. They're shared between command line and the library.

```bash
# @TODO add examples here
```
-->


## Command line Usage

### Quickstart

```bash
osmdicli --help

# test with examples from tests/data
osmdicli tests/data/example-005.osmdi.yml
```

## The proto specification for OSM data intent file

The general idea is based initial attempt to implement idea behind <https://docs.google.com/presentation/d/1V3gDPh5uzmIYtuPptFJY1GbfbvnxW_ViWuIsnSr9bhQ/edit?usp=sharing>.

Some early comments (2023-09-02) on _how_ to do it (subject to change):

- Focused on OpenStreetMap data and tooling.
  - _and_ it accepts input data from non OpenStreetMap data (for now, Wikidata) because allows to be used to explain relationship between concepts
    - yes, this means tools could explain how to dump data (for now, only SPARQL implemented) external to OpenStreetMap
    - the semantics on how to compare data does not have code implemented

### Reference codes at top level

For files with examples, check [tests/data](tests/data).

- `0`: metadata (optional)
- `1`: input data
- `2`: environment data (optional)
- `3`: output data (optional)

### `1`: input data
#### `1.1`: natural language expalantion, from developer to developer
#### `1.2`: natural language example of averange user query
#### `1.3`: OpenStreetMap tags for select data
#### `1.4`: OpenStreetMap tags for exclude data
#### `1.5`: OpenStreetMap Wikibase Data Item
#### `1.10`: Wikidata Wikibase Q items
#### `1.20`: operation inside place
##### `1.20.1`: operation inside place, parameter natural language
##### `1.20.2`: operation inside place, parameter OSM tagging
##### `1.20.3`: operation inside place, parameter OSM relation
##### `1.20.4`: operation inside place, parameter Wikidata concept
### `2`: environment data
#### `2.1` prefered natural languages (to restrict output if too many options)
### `3`: output data

# License

Public domain