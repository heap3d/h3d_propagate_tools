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

from h3d_propagate_tools.scripts.center_utilites import (
    update_instance,
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

    if not isinstance(newmesh, modo.Mesh) or not isinstance(oldmesh, modo.Mesh):
        raise TypeError('Both selected items must be mesh items.')

    update_instance(newmesh, oldmesh)


if __name__ == '__main__':
    main()
