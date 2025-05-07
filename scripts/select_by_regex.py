#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# select items with custom regex pattern
# ================================

import re
from typing import Any

import lx
import modo
import modo.constants as c


USERVAL_IGNORE_HIDDEN = 'h3d_propagate_ignore_hidden'
USERVAL_REGEX_PATTERN = 'h3d_propagate_regex'
REGEX_PATTERN = r'^(.*?)[._ (d)]*[ ().\d]*\d*\)?$'


def main():
    visible_only = bool(get_user_value(USERVAL_IGNORE_HIDDEN))
    selected_items = get_selected(visible_only)
    all_items = get_all_items(visible_only)

    similar_items: set[modo.Item] = set()

    for selected_item in selected_items:
        if selected_item in similar_items:
            continue

        for item in all_items:
            if item in similar_items:
                continue
            is_similar = is_name_similar(item.name, selected_item.name, get_user_value(USERVAL_REGEX_PATTERN))
            if is_similar:
                similar_items.add(item)

    for selected_item in similar_items:
        selected_item.select()


def get_user_value(name: str) -> Any:
    value = lx.eval("user.value {} ?".format(name))
    return value


def get_selected(visible: bool) -> list[modo.Item]:
    if visible:
        return [
            i
            for i in modo.Scene().selectedByType(itype=c.LOCATOR_TYPE, superType=True)
            if is_visible(i)
        ]
    else:
        return modo.Scene().selectedByType(itype=c.LOCATOR_TYPE, superType=True)


def is_visible(item: modo.Item) -> bool:
    if not is_local_visible(item):
        return False

    parents = item.parents
    if not parents:
        return True

    if any(map(lambda x: is_visible_alloff(x), parents)):
        return False

    return True


def is_visible_alloff(item: modo.Item) -> bool:
    visible_channel = item.channel('visible')
    if not visible_channel:
        return False

    visible = str(visible_channel.get())

    return visible == 'allOff'


def is_local_visible(item: modo.Item) -> bool:
    visible_channel = item.channel('visible')
    if not visible_channel:
        return False

    visible = str(visible_channel.get())
    visible_values = {
        'default': True,
        'on': True,
        'off': False,
        'allOff': False,
    }

    result = visible_values.get(visible, False)
    return result


def get_all_items(visible: bool) -> list[modo.Item]:
    if visible:
        return [
            item
            for item in modo.Scene().items(itype=c.LOCATOR_TYPE, superType=True)
            if is_visible(item)
        ]
    else:
        return [
            item
            for item in modo.Scene().items(itype=c.LOCATOR_TYPE, superType=True)
        ]


def is_name_similar(name: str, template: str, regex_pattern=REGEX_PATTERN) -> bool:
    template_match = re.search(regex_pattern, template)

    if not template_match:
        template_stripped = template
    else:
        if template_match.groups():
            template_stripped = template_match.group(1)
        else:
            start, end = template_match.span()
            template_stripped = template[start:end]

    name_match = re.search(regex_pattern, name)

    if not name_match:
        name_sripped = name
    else:
        if name_match.groups():
            name_sripped = name_match.group(1)
        else:
            start, end = name_match.span()
            name_sripped = name[start:end]

    if template_stripped.strip() == name_sripped.strip():
        return True

    return False


if __name__ == '__main__':
    main()
