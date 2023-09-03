from typing import List


def osmdi_langs_preferred(options: list, preferences: List[list] = None) -> list:
    """Decide which languages to load

    Args:
        options (list): List of availible alternatives to select
        preferences (List[list], optional): Preferences, if any. Defaults to None.

    Returns:
        list: the selected number of languages
    """
    if preferences is None or len(preferences) == 0:
        return options

    selected = []

    for block in preferences:
        block_done = False
        for block_item in block:
            if block_done is True:
                break
            for availible_option in options:
                if block_item.lower() == availible_option.lower():
                    selected.append(availible_option)
                    block_done = True
                    break
    return selected