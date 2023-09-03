# openstreetmap-data-intent, proof of concept
[early-draft] See https://docs.google.com/presentation/d/1V3gDPh5uzmIYtuPptFJY1GbfbvnxW_ViWuIsnSr9bhQ/edit?usp=sharing


## Installing

```bash
# pip install osmdi --upgrade
pip install git+https://github.com/fititnt/openstreetmap-data-intent.git#egg=osmdi
```

### Environment variables
Customize for your needs. They're shared between command line and the library.

```bash
# @TODO add examples here
```

## Command line Usage

### Quickstart

```bash
osmdicli tests/data/example-003.json
```

# The proto specification for OSM data intent file

The general idea is based initial attempt to implement idea behind <https://docs.google.com/presentation/d/1V3gDPh5uzmIYtuPptFJY1GbfbvnxW_ViWuIsnSr9bhQ/edit?usp=sharing>.

Some early comments (2023-09-02) on _how_ to do it (subject to change):

- Focused on OpenStreetMap data and tooling.
  - _and_ it accepts input data from non OpenStreetMap data (for now, Wikidata) because allows to be used to explain relationship between concepts
    - yes, this means tools could explain how to dump data (for now, only SPARQL implemented) external to OpenStreetMap
    - the semantics on how to compare data does not have code implemented

## Reference codes

### Top level

> The actual instructions, which aren't optional, are the input _`1`: input data_.

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
#### `1.20`: operation inside place, parameter natural language
#### `1.21`: operation inside place, parameter OSM tagging
#### `1.22`: operation inside place, parameter OSM relation
#### `1.23`: operation inside place, parameter Wikidata concept
### `2`: environment data
#### `2.1` prefered natural languages (to restrict output if too many options)