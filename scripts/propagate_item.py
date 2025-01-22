#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# Instance and align the last selected to the selected items
# ================================

import modo
import modo.constants as c

from h3d_propagate_tools.scripts.update_instances import make_instance
from h3d_propagate_tools.scripts.replace_with_instance import parent_items_to, match_pos_rot, get_parent_index


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

    for target in targets:
        instance_item = make_instance(source_item)
        match_pos_rot(instance_item, target)
        parent_items_to([instance_item,], target.parent, get_parent_index(target)+1)


if __name__ == '__main__':
    main()
