#!/usr/bin/python
# ================================
# (C)2025-2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# Replace selected items with the instance of last selected
# ================================

import modo
import modo.constants as c

from h3d_utilites.scripts.h3d_utils import (
    execution_time_alarm,
    match_pos_rot,
    match_scl,
    parent_items_to,
    get_parent_index,
    get_source_of_instance,
    get_instances,
    remove_if_exist,
    set_selection_mode,
    SELECTION_MODE,
    select_if_exists,
)


TMP_SUFFIX = '_tmp'

DIALOG_TITLE = 'Replace Items with Instance'
ERRMSG_SELECTMORE = 'Please select two or more items to run the command.'


@execution_time_alarm('Replace Items with Instance')
def main():
    scene = modo.Scene()
    selected = scene.selectedByType(c.LOCATOR_TYPE, superType=True)
    if len(selected) < 2:
        print(DIALOG_TITLE, ERRMSG_SELECTMORE)
        modo.dialogs.alert(DIALOG_TITLE, ERRMSG_SELECTMORE)
        return
    source = selected[-1]
    target_candidates = selected[:-1]

    targets_no_groups: set[modo.Item] = set(filter(lambda i: i.type != 'groupLocator', target_candidates))
    target_instances = {item: get_instances(item) for item in targets_no_groups}

    instances: set[modo.Item] = set()
    for item in target_instances:
        instances.update(target_instances[item])

    targets = targets_no_groups - instances

    new_items: list[modo.Item] = []
    for item in instances:
        new_items.append(duplicate_instance_and_align(source=source, target=item))

    for item in targets:
        new_items.append(duplicate_instance_and_align(source=source, target=item))

    for item in targets:
        remove_if_exist(item, children=True)

    set_selection_mode(SELECTION_MODE.ITEM.value)
    select_if_exists(new_items)


def duplicate_instance_and_align(source: modo.Item, target: modo.Item) -> modo.Item:
    if not source:
        raise ValueError('Source item error: value is None')
    if not target:
        raise ValueError('Target item error: value is None')

    instanced_item = modo.Scene().duplicateItem(item=get_source_of_instance(source), instance=True)
    if not instanced_item:
        raise ValueError('Failed to duplicate source_item')
    instance_name = target.name
    target.name = instance_name + TMP_SUFFIX
    instanced_item.name = instance_name
    instanced_item.setParent()
    match_pos_rot(instanced_item, target)
    match_scl(instanced_item, target)

    align_items(source=target, target=instanced_item)

    return instanced_item


def align_items(source: modo.Item, target: modo.Item):
    parent = source.parent
    children = source.children()

    parent_index = get_parent_index(source)
    parent_items_to([target,], parent, parent_index)
    parent_items_to(children, target)


if __name__ == '__main__':
    main()
