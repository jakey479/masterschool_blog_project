from typing import List, Dict, Union


def sort_list_of_dicts_by_value(
        list_of_dicts: List[Dict[str, Union[str, int]]],
        sort_direction: str,
        sort_key: str
) -> List[Dict[str, Union[str, int]]]:
    # depends on sort_key existing
    if sort_direction == 'asc':
        if sort_key == 'title':
            return sorted(list_of_dicts, key=lambda blog: blog['title'], reverse=True)
        elif sort_key == 'content':
            return sorted(list_of_dicts, key=lambda blog: blog['content'], reverse=True)
    if sort_direction == 'desc':
        if sort_key == 'title':
            return sorted(list_of_dicts, key=lambda blog: blog['title'], reverse=False)
        elif sort_key == 'content':
            return sorted(list_of_dicts, key=lambda blog: blog['content'], reverse=False)
