#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# Select a source of the instance item
# ================================

import modo

from h3d_utilites.scripts.h3d_utils import get_source_of_instance


def main():
    selected = modo.Scene().selected

    source_items: list[modo.Item] = []
    for item in selected:
        source = get_source_of_instance(item)
        if source:
            source_items.append(source)

    if not source_items:
        return

    modo.Scene().deselect()
    for item in source_items:
        item.select()


if __name__ == '__main__':
    main()
