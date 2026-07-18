#!/usr/bin/python
# ================================
# (C)2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# orient mesh center z-axis to selection normal
# ================================

import lx
import modo
import modo.constants as c

from h3d_propagate_tools.scripts.center_utilites import (
    get_selected_components,
    numparents,
    create_loc_at_selection,
    align_center_to_item,
)

from h3d_utilites.scripts.h3d_utils import (
    execution_time_alarm,
    select_components,
    parent_items_to,
    match_pos,
    get_selection_mode,
    set_selection_mode,
    select_if_exists,
    remove_if_exist,
    )


SELECTION_LOC = 'selection loc'
NORMAL_DIRECTION_LOC = 'normal direction loc'
RESULT_LOC = 'result loc'


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

        updated_mesh = orient_z_axis_to_normal(mesh, selection_mode)
        updated_meshes.append(updated_mesh)

    select_if_exists(updated_meshes)


def orient_z_axis_to_normal(mesh: modo.Mesh, selection_mode: str) -> modo.Mesh:
    selection_loc = create_loc_at_selection(mesh, selection_mode, SELECTION_LOC)

    normal_direction_loc = modo.Scene().addItem(itype=c.LOCATOR_TYPE, name=NORMAL_DIRECTION_LOC)
    parent_items_to((normal_direction_loc,), mesh, inplace=False)
    normal_direction_loc.select(replace=True)
    lx.eval('transform.channel pos.Y 0.1')
    parent_items_to((normal_direction_loc,), None, inplace=True)

    match_pos(selection_loc, mesh)

    selection_loc.select(replace=True)
    normal_direction_loc.select()
    lx.eval('constraintDirection')
    lx.eval('constraint.effect add')
    lx.eval('item.channel ceMatrix$opacity.X 0.0')
    lx.eval('item.channel ceMatrix$opacity.Z 0.0')

    result_loc = modo.Scene().addItem(itype=c.LOCATOR_TYPE, name=RESULT_LOC)
    parent_items_to((result_loc,), selection_loc, inplace=False)
    result_loc.select(replace=True)
    lx.eval('transform.channel rot.X -90.0')
    parent_items_to((result_loc,), None, inplace=True)

    updated_mesh = align_center_to_item(mesh, result_loc)

    remove_if_exist(normal_direction_loc, True)
    remove_if_exist(selection_loc, True)
    remove_if_exist(result_loc, True)

    return updated_mesh


if __name__ == '__main__':
    main()
