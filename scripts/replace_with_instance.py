#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# Replace selected items with the instance of last selected
# ================================

import modo
import modo.constants as c
import lx

from scripts.utilites import (
    match_pos_rot,
    match_scl,
    parent_items_to,
    get_parent_index,
    get_instance_source,
)


TMP_SUFFIX = '_tmp'

DIALOG_TITLE = 'Replace Items with Instance'
ERRMSG_SELECTMORE = 'Please select two or more items to run the command.'


def main():
    scene = modo.Scene()
    selected = scene.selectedByType(c.LOCATOR_TYPE, superType=True)
    if len(selected) < 2:
        print(DIALOG_TITLE, ERRMSG_SELECTMORE)
        modo.dialogs.alert(DIALOG_TITLE, ERRMSG_SELECTMORE)
        return
    source = selected[-1]
    target_candidates = selected[:-1]
    targets = tuple(filter(lambda i: i.type != 'groupLocator', target_candidates))

    new_items: list[modo.Item] = []
    for target in targets:
        new_items.append(replace_with_instance(source_item=source, target_item=target))

    for item in target_candidates:
        try:
            modo.Scene().removeItems(item, children=True)
        except LookupError:
            print('removeItemsError')

    lx.eval('select.type item')
    modo.Scene().deselect()
    for item in new_items:
        item.select()


def replace_with_instance(source_item: modo.Item, target_item: modo.Item) -> modo.Item:
    if not source_item:
        raise ValueError('Source item error: value is None')
    if not target_item:
        raise ValueError('Target item error: value is None')
    instance_item = modo.Scene().duplicateItem(
        item=get_instance_source(source_item), instance=True
    )
    if not instance_item:
        raise ValueError('Failed to duplicate source_item')
    instance_name = target_item.name
    target_item.name = instance_name + TMP_SUFFIX
    instance_item.name = instance_name
    instance_item.setParent()
    match_pos_rot(instance_item, target_item)
    match_scl(instance_item, target_item)

    replace_item(remove_item=target_item, insert_item=instance_item)

    return instance_item


def replace_item(remove_item: modo.Item, insert_item: modo.Item):
    parent = remove_item.parent
    children = remove_item.children()
    parent_index = get_parent_index(remove_item)
    parent_items_to([insert_item,], parent, parent_index)
    parent_items_to(children, insert_item)


if __name__ == '__main__':
    main()
