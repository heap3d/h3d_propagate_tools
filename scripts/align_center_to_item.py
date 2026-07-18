#!/usr/bin/python
# ================================
# (C)2025-2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# Leonard
# align mesh center position and rotation to last selected item
# ================================

from typing import Iterable

import modo
import modo.constants as c

from h3d_propagate_tools.scripts.center_utilites import (
    numparents,
    align_center_to_item,
)

from h3d_utilites.scripts.h3d_utils import (
    execution_time_alarm,
    itype_str,
    select_if_exists,
    )


@execution_time_alarm('Set Item Center > Aligned To Item')
def main():
    selected = modo.Scene().selectedByType(itype=c.LOCATOR_TYPE, superType=True)
    if len(selected) < 2:
        print('Select at least one mesh and one target locator.')
        return

    target_item = selected[-1]
    source_items = [item for item in selected[:-1] if item.type == itype_str(c.MESH_TYPE)]
    source_items.sort(key=numparents, reverse=True)

    if not source_items:
        return

    updated_items: list[modo.Mesh] = []
    for source_item in source_items:
        updated_items.append(align_center_to_item(source_item, target_item))

    select_if_exists(updated_items)


if __name__ == '__main__':
    main()
