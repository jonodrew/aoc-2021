from typing import Dict, Tuple, Any, Union, FrozenSet, List


def combine_dicts(first_dict: Dict[Any, Union[int, List, Tuple]], second_dict: Dict[Any, Union[int, List, Tuple]]) -> Dict[Any, Union[int, List, Tuple]]:
    """
    Combine two dictionaries.
    :param first_dict:
    :param second_dict:
    :return:
    """
    if not second_dict:
        return first_dict
    else:
        new_key, new_value = second_dict.popitem()
        return combine_dicts(update_dict(first_dict, new_key, new_value), second_dict)


def update_dict(dict_to_update: Dict[Any, Union[int, List, Tuple]], key: Any, value: Union[int, List, Tuple]) -> Dict[Any, Union[int, List, Tuple]]:
    """
    This function only works with dicts whose values are `int`s, lists, or tuples.
    :param dict_to_update:
    :param key:
    :param value:
    :return:
    """
    if type(value) not in (tuple, list, int):
        raise ValueError
    if key in dict_to_update.keys():
        return {old_key: (old_value if old_key != key else old_value + value) for old_key, old_value in dict_to_update.items()}
    else:
        return {**dict_to_update, key:value}


def reduce_frozen_set_to_dict(impacted_dict: Union[None, Dict[Tuple[int, int], int]], impacted_frozenset: FrozenSet) -> Dict[Tuple[int, int], int]:
    new_impacted = {coords: 1 for coords in impacted_frozenset}
    if impacted_dict is None:
        return new_impacted
    else:
        return combine_dicts(new_impacted, impacted_dict)