#!/usr/bin/python
# ================================
# (C)2025-2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# EMAG
# set item center position and orientation by component selection
# ================================

import modo
import modo.constants as c

from h3d_utilites.scripts.h3d_utils import (
    get_selection_mode,
    select_if_exists,
    execution_time_alarm,
)

from h3d_propagate_tools.scripts.center_utilites import (
    get_selected_components,
    numparents,
    create_loc_at_selection,
    select_components,
)


@execution_time_alarm('Set Item Center > Aligned To Selection')
def main():
    selected_meshes: list[modo.Mesh] = modo.Scene().selectedByType(itype=c.MESH_TYPE)
    selected_meshes.sort(key=numparents, reverse=True)
    if not selected_meshes:
        return

    select_type = get_selection_mode()
    selected_components: dict[modo.Mesh, list] = dict()
    for mesh in selected_meshes:
        selected_components[mesh] = get_selected_components(mesh, select_type)

    new_locators: list[modo.Item] = []
    for mesh in selected_meshes:
        if not mesh.geometry.numVertices:
            continue

        select_components(mesh, select_type, selected_components[mesh])
        new_locator = create_loc_at_selection(mesh, select_type)

        new_locators.append(new_locator)

    select_if_exists(new_locators)


if __name__ == '__main__':
    main()
