import json
import yaml


def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, str_presenter)
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)


def yaml_dumper(data) -> str:
    """Convert abstract data into string, with optionated YAML style

    Args:
        data (Any): input data to export as string

    Returns:
        str: the output
    """
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


def json_dumper(data) -> str:
    """Convert abstract data into pretty printed JSON string

    Args:
        data (Any): input data to export as string

    Returns:
        str: the output
    """
    return json.dumps(data, ensure_ascii=False, indent=2)
