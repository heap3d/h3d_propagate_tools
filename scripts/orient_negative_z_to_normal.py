#!/usr/bin/python
# ================================
# (C)2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# orient mesh center negative z-axis to selection normal
# ================================

import modo
import modo.constants as c

from h3d_propagate_tools.scripts.center_utilites import (
    get_selected_components,
    numparents,
    orient_z_axis_to_normal,
)

from h3d_utilites.scripts.h3d_utils import (
    execution_time_alarm,
    select_components,
    get_selection_mode,
    set_selection_mode,
    select_if_exists,
    )


@execution_time_alarm('Set Item Center > Z-Axis to Normal')
def main():
    selected_meshes: list[modo.Mesh] = modo.Scene().selectedByType(itype=c.MESH_TYPE)
    selected_meshes.sort(key=numparents, reverse=True)
    if not selected_meshes:
        return

    selection_mode = get_selection_mode()
    selected_components: dict[modo.Mesh, list] = dict()
    for mesh in selected_meshes:
        selected_components[mesh] = get_selected_components(mesh, selection_mode)

    updated_meshes: list[modo.Mesh] = []
    for mesh in selected_meshes:
        if not mesh.geometry.numVertices:
            continue

        set_selection_mode(selection_mode)
        select_components(selected_components[mesh])

        updated_mesh = orient_z_axis_to_normal(mesh, selection_mode, flip=True)
        updated_meshes.append(updated_mesh)

    select_if_exists(updated_meshes)


if __name__ == '__main__':
    main()
