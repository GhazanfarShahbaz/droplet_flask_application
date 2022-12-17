from typing import List

from repository.model import Class


def class_type_list_to_event_dict_list(class_list: List[Class]) -> List[dict]:
    """
    Converts class type list to an event dictionary for responses

    Returns:
        List[dict]: A list of assignmnents in dictionary form
    """
    return [_class.to_dict() for _class in class_list]
