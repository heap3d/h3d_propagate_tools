#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# select items with similar name
# ================================

import modo

from scripts.utilites import (
    get_user_value,
)

from scripts.center_utilites import (
    USERVAL_IGNORE_HIDDEN,
    get_selected,
    get_all_items,
    is_name_similar,
)


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
            is_similar = is_name_similar(item.name, selected_item.name)
            if is_similar:
                similar_items.add(item)

    for selected_item in similar_items:
        selected_item.select()


if __name__ == '__main__':
    main()
