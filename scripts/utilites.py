#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# EMAG
# utilites for propagate tools
# ================================

from typing import Optional, Any

import modo
import lx


ITEM = 'item'
VERTEX = 'vertex'
EDGE = 'edge'
POLYGON = 'polygon'

COLOR_PROCESSED = 'orange'


def parent_items_to(items: list[modo.Item], parent: Optional[modo.Item], index=0, inplace=True):
    inplace_num = 1 if inplace else 0
    for item in items:
        if not parent:
            lx.eval(f"item.parent item:{{{item.id}}} parent:{{}} position:{index} inPlace:{inplace_num}")
        else:
            lx.eval(f"item.parent item:{{{item.id}}} parent:{{{parent.id}}} position:{index} inPlace:{inplace_num}")


def get_parent_index(item: modo.Item) -> int:
    if index := item.parentIndex:
        return index
    if index := item.rootIndex:
        return index
    return 0


def match_pos_rot(item: modo.Item, itemTo: modo.Item):
    lx.eval(f'item.match item pos average:false item:{{{item.id}}} itemTo:{{{itemTo.id}}}')
    lx.eval(f'item.match item rot average:false item:{{{item.id}}} itemTo:{{{itemTo.id}}}')


def match_scl(item: modo.Item, itemTo: modo.Item):
    lx.eval(f'item.match item scl average:false item:{{{item.id}}} itemTo:{{{itemTo.id}}}')


def get_instances(item: modo.Item) -> list[modo.Item]:
    instances = item.itemGraph('source').reverse()
    if not isinstance(instances, list):
        raise ValueError(f'Error getting instances for the <{item.name}> item')
    return instances


def make_instance(item: modo.Item) -> modo.Item:
    item.select(replace=True)
    lx.eval('item.duplicate true all:true')
    newitem = modo.Scene().selected[0]
    return newitem


def duplicate_item(item: modo.Item) -> modo.Item:
    if not item:
        raise TypeError('No item provided.')

    copy = modo.Scene().duplicateItem(item)
    if not copy:
        raise TypeError('Item duplication error.')

    return copy


def get_user_value(name: str) -> Any:
    """gets user value by name

    Args:
        name (str): user value name

    Returns:
        Any: user value
    """
    value = lx.eval('user.value {} ?'.format(name))
    return value
