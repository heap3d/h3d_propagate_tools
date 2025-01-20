#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# Instance and align the last selected to the selected items. The two last selected items define the offset.
# ================================

import lx
import modo
import modo.constants as c
from modo.mathutils import Vector3

from h3d_propagate_tools.scripts.replace_with_instance import match_pos_rot, match_scl


class Offset:
    def __init__(self, pos: Vector3, rot: Vector3, scl: Vector3):
        self.pos = pos
        self.rot = rot
        self.scl = scl


def main():
    selected = modo.Scene().selectedByType(itype=c.LOCATOR_TYPE, superType=True)
    offset_item = selected[-2]
    source_item = selected[-1]
    targets = selected[:-1]

    offset = get_offset(source=offset_item, target=source_item)

    for target in targets:
        instance_item = instance(target, children=True)
        match_pos_rot(instance_item, target)
        match_scl(instance_item, target)
        apply_offset(instance_item, offset)


def get_offset(source: modo.Item, target: modo.Item) -> Offset:
    pos = get_pos(target) - get_pos(source)
    rot = get_rot(target) - get_rot(source)
    scl: Vector3 = Vector3(0, 0, 0)
    try:
        scl.x = get_scl(target).x / get_scl(source).x
    except ZeroDivisionError:
        scl.x = 1
    try:
        scl.y = get_scl(target).y / get_scl(source).y
    except ZeroDivisionError:
        scl.y = 1
    try:
        scl.z = get_scl(target).z / get_scl(source).z
    except ZeroDivisionError:
        scl.z = 1

    return Offset(pos, rot, scl)


def get_pos(item: modo.Item) -> Vector3:
    x = lx.eval(f'transform.channel pos.X ? item:{{{item.id}}}')
    if x is None:
        x = 0
    y = lx.eval(f'transform.channel pos.Y ? item:{{{item.id}}}')
    if y is None:
        y = 0
    z = lx.eval(f'transform.channel pos.Z ? item:{{{item.id}}}')
    if z is None:
        z = 0

    return Vector3(x, y, z)


def get_rot(item: modo.Item) -> Vector3:
    x = lx.eval(f'transform.channel rot.X ? item:{{{item.id}}}')
    if x is None:
        x = 0
    y = lx.eval(f'transform.channel rot.Y ? item:{{{item.id}}}')
    if y is None:
        y = 0
    z = lx.eval(f'transform.channel rot.Z ? item:{{{item.id}}}')
    if z is None:
        z = 0

    return Vector3(x, y, z)


def get_scl(item: modo.Item) -> Vector3:
    x = lx.eval(f'transform.channel scl.X ? item:{{{item.id}}}')
    if x is None:
        x = 1
    y = lx.eval(f'transform.channel scl.Y ? item:{{{item.id}}}')
    if y is None:
        y = 1
    z = lx.eval(f'transform.channel scl.Z ? item:{{{item.id}}}')
    if z is None:
        z = 1

    return Vector3(x, y, z)


def instance(item: modo.Item, children: bool) -> modo.Item:
    ...


def apply_offset(item: modo.Item, offset: Offset):
    ...


if __name__ == '__main__':
    main()
