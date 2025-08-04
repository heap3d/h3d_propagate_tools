#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# Select a source of the instance item
# ================================

import modo

from h3d_propagate_tools.scripts.center_utilites import get_instance_source


def main():
    selected = modo.Scene().selected

    source_items: list[modo.Item] = []
    for item in selected:
        source = get_instance_source(item)
        if source:
            source_items.append(source)

    if not source_items:
        return

    modo.Scene().deselect()
    for item in source_items:
        item.select()


if __name__ == '__main__':
    main()
