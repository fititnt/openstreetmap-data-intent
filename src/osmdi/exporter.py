import yaml


def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, str_presenter)

# to use with safe_dump:
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)


def yaml_dumper(data) -> str:
    # @see https://stackoverflow.com/questions/8640959/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data
    return yaml.dump(
        data,
        allow_unicode=True,
        indent=2,
        # width=80,
        sort_keys=True,
        default_flow_style=False,
        line_break=True,
    )
