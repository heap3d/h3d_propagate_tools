#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# Instance and align the last selected to the selected items
# ================================

from typing import Iterable

import modo
import modo.constants as c

from scripts.utilites import (
    make_instance,
    match_pos_rot,
    parent_items_to,
    get_parent_index,
)


DIALOG_TITLE = 'Propagate Item'
ERRMSG_SELECTMORE = 'Please select two or more items to run the command.'


def main():
    selected = modo.Scene().selectedByType(itype=c.LOCATOR_TYPE, superType=True)
    if len(selected) < 2:
        print(DIALOG_TITLE, ERRMSG_SELECTMORE)
        modo.dialogs.alert(DIALOG_TITLE, ERRMSG_SELECTMORE)
        return
    source_item: modo.Item = selected[-1]
    targets: list[modo.Item] = selected[:-1]

    make_aligned_instances(source_item, targets)


def make_aligned_instances(source: modo.Item, targets: Iterable) -> tuple[modo.Item, ...]:
    instances: set[modo.Item] = set()
    for target in targets:
        instance_item = make_instance(source)
        instances.add(instance_item)
        match_pos_rot(instance_item, target)
        parent_items_to([instance_item,], target.parent, get_parent_index(target)+1)

    return tuple(instances)


if __name__ == '__main__':
    main()
