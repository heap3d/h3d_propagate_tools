#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# Select a source of the instance item
# ================================

from typing import Union

import modo


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


def get_instance_source(instance: modo.Item) -> Union[None, modo.Item]:
    try:
        return instance.itemGraph('source').forward()[0]  # type:ignore
    except IndexError:
        return None


if __name__ == '__main__':
    main()
