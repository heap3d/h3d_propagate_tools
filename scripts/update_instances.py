#!/usr/bin/python
# ================================
# (C)2025-2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# replace source of instances without changing their position
# ================================

import modo
import modo.constants as c

from h3d_propagate_tools.scripts.center_utilites import update_instance

from h3d_utilites.scripts.h3d_utils import execution_time_alarm, select_if_exists


DIALOG_TITLE = 'Update Instances'
ERRMSG_SELECT2MESHES = 'Please select two mesh items to run the command.'


@execution_time_alarm('Update Instances')
def main():
    selected = modo.Scene().selectedByType(itype=c.MESH_TYPE)
    if len(selected) < 2:
        print(DIALOG_TITLE, ERRMSG_SELECT2MESHES)
        modo.dialogs.alert(DIALOG_TITLE, ERRMSG_SELECT2MESHES)
        return

    newmesh: modo.Mesh = selected[-1]
    oldmesh: modo.Mesh = selected[-2]

    updated_items = update_instance(newmesh, oldmesh)
    select_if_exists(updated_items)


if __name__ == '__main__':
    main()
