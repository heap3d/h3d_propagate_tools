#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# replace source of instances without changing their position
# ================================

import modo
import modo.constants as c

from scripts.utilites import (
    match_pos_rot,
    parent_items_to,
    get_parent_index,
    get_instances,
    make_instance,
)


DIALOG_TITLE = 'Update Instances'
ERRMSG_SELECT2MESHES = 'Please select two mesh items to run the command.'


def main():
    selected = modo.Scene().selectedByType(itype=c.MESH_TYPE)
    if len(selected) < 2:
        print(DIALOG_TITLE, ERRMSG_SELECT2MESHES)
        modo.dialogs.alert(DIALOG_TITLE, ERRMSG_SELECT2MESHES)
        return

    newmesh: modo.Item = selected[-2]
    oldmesh: modo.Item = selected[-1]
    targets = get_instances(oldmesh)

    parent_items_to([newmesh,], oldmesh.parent, get_parent_index(oldmesh))

    tmp_loc = modo.Scene().addItem(itype='locator')
    for target in targets:
        instance_item = make_instance(newmesh)

        match_pos_rot(tmp_loc, oldmesh)
        parent_items_to([instance_item,], tmp_loc)

        match_pos_rot(tmp_loc, target)
        parent_items_to([instance_item,], target.parent, get_parent_index(target))

    modo.Scene().removeItems(tmp_loc)
    modo.Scene().removeItems(oldmesh, children=True)


if __name__ == '__main__':
    main()
