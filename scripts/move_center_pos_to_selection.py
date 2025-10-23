#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# Leonard
# move item center position by component selection
# ================================

import modo
import modo.constants as c
import lx

from h3d_propagate_tools.scripts.utilites import (
    get_select_type,
    duplicate_item_and_hierarchy,
    parent_items_to,
    get_parent_index,
    match_pos,
    match_pos_rot,
)

from h3d_propagate_tools.scripts.center_utilites import (
    get_selected_components,
    select_components,
    create_loc_at_selection,
    update_instance,
    place_center_at_locator,
)


def main():
    selected_meshes: list[modo.Mesh] = modo.Scene().selectedByType(itype=c.MESH_TYPE)
    select_type = get_select_type()

    selected_components: dict[modo.Mesh, list] = dict()
    for mesh in selected_meshes:
        selected_components[mesh] = get_selected_components(mesh, select_type)

    new_meshes: list[modo.Mesh] = []
    for mesh in selected_meshes:
        if not mesh.geometry.numVertices:
            continue

        original_parent = mesh.parent
        original_parent_index = get_parent_index(mesh)
        select_components(mesh, selected_components[mesh], select_type)

        original_loc: modo.Item = modo.Scene().addItem(itype=c.LOCATOR_TYPE, name='original_loc')
        if not original_loc:
            raise RuntimeError('Failed to create locator.')

        match_pos_rot(original_loc, mesh)

        mesh.select(replace=True)
        lx.eval('transform.reset all')

        selection_center_loc = create_loc_at_selection(mesh, select_type, orient=False)
        selection_center_loc.name = 'selection_center_loc'

        legacy_center_loc = modo.Scene().addItem(itype=c.LOCATOR_TYPE, name='legacy_center_loc')
        match_pos_rot(legacy_center_loc, mesh)

        new_center_loc = duplicate_item_and_hierarchy(legacy_center_loc)
        new_center_loc.name = 'new_center_loc'

        match_pos(new_center_loc, selection_center_loc)
        modo.Scene().removeItems(selection_center_loc)

        parent_items_to((new_center_loc,), mesh, inplace=True)
        parent_items_to((mesh,), original_loc, inplace=False)
        parent_items_to((mesh,), original_parent, index=original_parent_index, inplace=True)
        modo.Scene().removeItems(original_loc)
        modo.Scene().removeItems(legacy_center_loc)

        new_mesh = duplicate_item_and_hierarchy(mesh)
        if not isinstance(new_mesh, modo.Mesh):
            raise TypeError('Failed to duplicate mesh.')

        place_center_at_locator(new_mesh, new_center_loc)
        modo.Scene().removeItems(new_center_loc)

        update_instance(new_mesh, mesh)

        new_meshes.append(new_mesh)

    if new_meshes:
        modo.Scene().deselect()
        for mesh in new_meshes:
            mesh.select()


if __name__ == '__main__':
    main()
