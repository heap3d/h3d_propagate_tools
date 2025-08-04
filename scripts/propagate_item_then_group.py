#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# Instance and align the last selected to the selected items. Group newly created instances
# ================================

from typing import Iterable

import lx
import modo
import modo.constants as c


from scripts.propagate_item import DIALOG_TITLE, ERRMSG_SELECTMORE, make_aligned_instances
from scripts.utilites import parent_items_to, get_parent_index


def main():
    selected = modo.Scene().selectedByType(itype=c.LOCATOR_TYPE, superType=True)
    if len(selected) < 2:
        print(DIALOG_TITLE, ERRMSG_SELECTMORE)
        modo.dialogs.alert(DIALOG_TITLE, ERRMSG_SELECTMORE)
        return
    source_item: modo.Item = selected[-1]
    targets: list[modo.Item] = selected[:-1]

    instances = make_aligned_instances(source_item, targets)
    group_items(instances, source_item)


def group_items(items: Iterable[modo.Item], source: modo.Item):
    modo.Scene().deselect()
    for item in items:
        item.select()

    lx.eval('layer.groupSelected')
    lx.eval(f'item.name {{{source.name} instances}}')
    grouploc = modo.Scene().selectedByType(itype=c.GROUPLOCATOR_TYPE)[0]
    parent_items_to([grouploc,], source.parent, get_parent_index(source))


if __name__ == '__main__':
    main()
