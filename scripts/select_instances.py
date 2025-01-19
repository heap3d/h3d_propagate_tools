#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# Select instances of the selected item
# ================================

import modo


def main():
    selected = modo.Scene().selected

    items_used: list[modo.Item] = []
    for item in selected:
        items_used.extend(get_instances(item))

    if not items_used:
        return

    modo.Scene().deselect()
    for item in items_used:
        item.select()


def get_instances(item: modo.Item) -> list[modo.Item]:
    instances = item.itemGraph('source').reverse()
    if not isinstance(instances, list):
        raise ValueError(f'Error getting instances for the <{item.name}> item')
    return instances


if __name__ == '__main__':
    main()
