#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# Propagate children of the last selected to the children of selected items
# ================================

import modo
import modo.constants as c

from h3d_propagate_tools.scripts.update_instances import make_instance
from h3d_propagate_tools.scripts.replace_with_instance import parent_items_to


CMD_NAME = 'Propagate Children'
ERRMSG_SELECT_MORE = 'Please select two or more items to run the command'
ERRMSG_SELECT_CHILDREN = 'The last selected item should contain children items. '\
    'Please select an item with children to run the command.'


def main():
    selected = modo.Scene().selectedByType(itype=c.LOCATOR_TYPE, superType=True)
    if len(selected) < 2:
        modo.dialogs.alert(CMD_NAME, ERRMSG_SELECT_MORE)
        return
    host_item: modo.Item = selected[-1]
    targets: list[modo.Item] = selected[:-1]

    if not host_item.children():
        modo.dialogs.alert(CMD_NAME, ERRMSG_SELECT_CHILDREN)
        return

    for target in targets:
        instance_item = make_instance(host_item)
        children = instance_item.children()
        parent_items_to(children, target, inplace=False)
        modo.Scene().removeItems(instance_item)


if __name__ == '__main__':
    main()
