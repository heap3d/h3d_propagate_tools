#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# Replace selected items with the instance of last selected
# ================================

from typing import Union

import modo
import modo.constants as c
import lx

from h3d_propagate_tools.scripts.select_source_of_instance import get_instance_source

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
    targets = filter(lambda i: i.type != 'groupLocator', target_candidates)

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
    match_scl(instance_item, get_instance_source(source_item))
    set_scale_factor(instance_item, get_ratios(source_item, target_item))

    replace_item(remove_item=target_item, insert_item=instance_item)

    return instance_item


def replace_item(remove_item: modo.Item, insert_item: modo.Item):
    parent = remove_item.parent
    children = remove_item.children()
    parent_index = get_parent_index(remove_item)
    parent_items_to([insert_item,], parent, parent_index)
    parent_items_to(children, insert_item)


def get_parent_index(item: modo.Item) -> int:
    if index := item.parentIndex:
        return index
    if index := item.rootIndex:
        return index
    return 0


def parent_items_to(items: list[modo.Item], parent: Union[None, modo.Item], index=0, inplace=True):
    inplace_num = 1 if inplace else 0
    for item in items:
        if not parent:
            lx.eval(f"item.parent item:{{{item.id}}} parent:{{}} position:{index} inPlace:{inplace_num}")
        else:
            lx.eval(f"item.parent item:{{{item.id}}} parent:{{{parent.id}}} position:{index} inPlace:{inplace_num}")


def match_pos_rot(item: modo.Item, itemTo: modo.Item):
    lx.eval(f'item.match item pos average:false item:{{{item.id}}} itemTo:{{{itemTo.id}}}')
    lx.eval(f'item.match item rot average:false item:{{{item.id}}} itemTo:{{{itemTo.id}}}')


def match_scl(item: modo.Item, itemTo: modo.Item):
    lx.eval(f'item.match item scl average:false item:{{{item.id}}} itemTo:{{{itemTo.id}}}')


def get_ratios(source: modo.Item, target: modo.Item) -> list[float]:
    source_size = get_source_size(source)
    target_size = get_size(target)

    if any([f == 0.0 for f in (source_size + target_size)]):
        ratio_x = 1.0
        ratio_y = 1.0
        ratio_z = 1.0
    else:
        ratio_x = target_size[0] / source_size[0]
        ratio_y = target_size[1] / source_size[1]
        ratio_z = target_size[2] / source_size[2]

    return [ratio_x, ratio_y, ratio_z]


def get_source_size(source: modo.Item) -> list[float]:
    source_scl_x, source_scl_y, source_scl_z = get_item_scale(source)
    base_scl_x, base_scl_y, base_scl_z = get_size(get_instance_source(source))
    source_size = [base_scl_x * source_scl_x, base_scl_y * source_scl_y, base_scl_z * source_scl_z]

    return source_size


def get_size(item: modo.Item) -> list[float]:
    if item.type != 'mesh' and item.type != 'meshInst':
        return [0.0, 0.0, 0.0]

    s_x, s_y, s_z = get_item_scale(item)
    if item.type == 'meshInst':
        corners = get_instance_source(item).geometry.boundingBox
    else:
        corners = item.geometry.boundingBox
    size_x = abs(corners[1][0] - corners[0][0]) * s_x
    size_y = abs(corners[1][1] - corners[0][1]) * s_y
    size_z = abs(corners[1][2] - corners[0][2]) * s_z

    return [size_x, size_y, size_z]


def get_item_scale(item: modo.Item) -> list[float]:
    item.select(replace=True)
    x = lx.eval(f'transform.channel scl.X ? item:{{{item.id}}}')
    if x is None:
        x = 1.0
    y = lx.eval(f'transform.channel scl.Y ? item:{{{item.id}}}')
    if y is None:
        y = 1.0
    z = lx.eval(f'transform.channel scl.Z ? item:{{{item.id}}}')
    if z is None:
        z = 1.0

    return [x, y, z]


def set_scale_factor(item: modo.Item, factor: list[float]):
    s_x, s_y, s_z = get_item_scale(item)
    set_item_scale(item, [s_x * factor[0], s_y * factor[1], s_z * factor[2]])


def set_item_scale(item: modo.Item, scale: list[float]):
    lx.eval(f'transform.channel scl.X {scale[0]} item:{{{item.id}}}')
    lx.eval(f'transform.channel scl.Y {scale[1]} item:{{{item.id}}}')
    lx.eval(f'transform.channel scl.Z {scale[2]} item:{{{item.id}}}')


if __name__ == '__main__':
    main()
