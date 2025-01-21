#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# replace source of instances without changing their position
# ================================

from math import degrees

import lx
import modo
import modo.constants as c
from modo.mathutils import Vector3

from h3d_propagate_tools.scripts.replace_with_instance import match_pos_rot, match_scl
from h3d_propagate_tools.scripts.select_instances import get_instances

from h3d_utilites.scripts.h3d_debug import h3dd, prints, fn_in, fn_out


class Offset:
    def __init__(self, pos: Vector3, rot: Vector3, scl: Vector3):
        self.pos = pos
        self.rot = rot
        self.scl = scl


def main():
    selected = modo.Scene().selectedByType(itype=c.MESH_TYPE)
    newmesh = selected[0]
    oldmesh = selected[1]
    targets = get_instances(oldmesh)

    offset = get_offset(source=oldmesh, target=newmesh)

    for target in targets:
        instance_item = instance(newmesh)
        match_pos_rot(instance_item, target)
        match_scl(instance_item, target)
        apply_offset(instance_item, offset)

    # modo.Scene().removeItems(oldmesh, children=True)


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


def instance(item: modo.Item) -> modo.Item:
    item.select(replace=True)
    lx.eval('item.duplicate true all:true')
    newitem = modo.Scene().selected[0]
    return newitem


def apply_offset(item: modo.Item, offset: Offset):
    pos = get_pos(item)
    rot = get_rot(item)
    scl = get_scl(item)

    new_pos = pos + offset.pos

    new_rot: Vector3 = Vector3()
    new_rot.x = rot.x + offset.rot.x
    new_rot.y = rot.y + offset.rot.y
    new_rot.z = rot.z + offset.rot.z

    new_scl: Vector3 = Vector3()
    new_scl.x = scl.x * offset.scl.x
    new_scl.y = scl.y * offset.scl.y
    new_scl.z = scl.z * offset.scl.z

    set_pos(item, new_pos)
    set_rot(item, new_rot)
    set_scl(item, new_scl)


def set_pos(item: modo.Item, pos: Vector3):
    lx.eval(f'transform.channel pos.X {pos.x} item:{{{item.id}}}')
    lx.eval(f'transform.channel pos.Y {pos.y} item:{{{item.id}}}')
    lx.eval(f'transform.channel pos.Z {pos.z} item:{{{item.id}}}')


def set_rot(item: modo.Item, rot: Vector3):
    lx.eval(f'transform.channel rot.X {degrees(rot.x)} item:{{{item.id}}}')
    lx.eval(f'transform.channel rot.Y {degrees(rot.y)} item:{{{item.id}}}')
    lx.eval(f'transform.channel rot.Z {degrees(rot.z)} item:{{{item.id}}}')


def set_scl(item: modo.Item, scl: Vector3):
    lx.eval(f'transform.channel scl.X {scl.x} item:{{{item.id}}}')
    lx.eval(f'transform.channel scl.Y {scl.y} item:{{{item.id}}}')
    lx.eval(f'transform.channel scl.Z {scl.z} item:{{{item.id}}}')


if __name__ == '__main__':
    h3dd.enable_debug_output()
    main()
