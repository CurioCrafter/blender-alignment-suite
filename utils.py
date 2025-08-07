import math
from typing import Iterable, List, Optional, Sequence, Tuple

import bpy
import bmesh
from mathutils import Matrix, Vector


AXES = ("X", "Y", "Z")


def axis_index(axis: str) -> int:
    axis = axis.upper()
    return {"X": 0, "Y": 1, "Z": 2}[axis]


def world_bounds_of_object(obj: bpy.types.Object) -> Tuple[Vector, Vector]:
    if not obj.data or not hasattr(obj.data, "vertices"):
        # Fallback to object origin as degenerate bounds
        w = obj.matrix_world.translation
        return Vector((w.x, w.y, w.z)), Vector((w.x, w.y, w.z))

    mat = obj.matrix_world
    corners = [mat @ Vector(corner) for corner in obj.bound_box]
    min_v = Vector((min(v.x for v in corners), min(v.y for v in corners), min(v.z for v in corners)))
    max_v = Vector((max(v.x for v in corners), max(v.y for v in corners), max(v.z for v in corners)))
    return min_v, max_v


def world_bounds_of_objects(objs: Iterable[bpy.types.Object]) -> Tuple[Vector, Vector]:
    mins: Optional[Vector] = None
    maxs: Optional[Vector] = None
    for obj in objs:
        mn, mx = world_bounds_of_object(obj)
        if mins is None:
            mins, maxs = mn.copy(), mx.copy()
        else:
            mins.x = min(mins.x, mn.x)
            mins.y = min(mins.y, mn.y)
            mins.z = min(mins.z, mn.z)
            maxs.x = max(maxs.x, mx.x)
            maxs.y = max(maxs.y, mx.y)
            maxs.z = max(maxs.z, mx.z)
    if mins is None:
        zero = Vector((0.0, 0.0, 0.0))
        return zero, zero
    return mins, maxs  # type: ignore[return-value]


def selected_objects(context: bpy.types.Context) -> List[bpy.types.Object]:
    return [obj for obj in context.selected_objects if obj and obj.type in {"MESH", "EMPTY", "LIGHT", "CAMERA", "CURVE", "FONT", "GPENCIL", "ARMATURE"}]


def active_object(context: bpy.types.Context) -> Optional[bpy.types.Object]:
    return context.view_layer.objects.active


def cursor_location(context: bpy.types.Context) -> Vector:
    return context.scene.cursor.location.copy()


def alignment_target_value(
    context: bpy.types.Context,
    axis: str,
    mode: str,
    objs: Optional[Sequence[bpy.types.Object]] = None,
) -> float:
    idx = axis_index(axis)
    mode = mode.upper()
    if mode == "WORLD":
        return 0.0
    if mode == "CURSOR":
        return cursor_location(context)[idx]

    if objs is None:
        objs = selected_objects(context)

    if not objs:
        return 0.0

    if mode == "ACTIVE":
        act = active_object(context)
        if not act:
            act = objs[0]
        mn, mx = world_bounds_of_object(act)
        return 0.5 * (mn[idx] + mx[idx])

    mn_all, mx_all = world_bounds_of_objects(objs)

    if mode == "MIN":
        return float(mn_all[idx])
    if mode == "MAX":
        return float(mx_all[idx])
    # CENTER / MEDIAN
    return 0.5 * (mn_all[idx] + mx_all[idx])


def set_object_world_location_axis(obj: bpy.types.Object, axis: str, value: float, use_bounds: bool, which_bound: str = "CENTER") -> None:
    idx = axis_index(axis)
    if not use_bounds:
        # Set world translation component directly to avoid parent/constraint confusion
        mw = obj.matrix_world.copy()
        tr = mw.translation.copy()
        tr[idx] = value
        mw.translation = tr
        obj.matrix_world = mw
        return

    # Align using bounding box: move so that min/center/max equals value
    mn, mx = world_bounds_of_object(obj)
    current = 0.5 * (mn[idx] + mx[idx])
    if which_bound == "MIN":
        current = mn[idx]
    elif which_bound == "MAX":
        current = mx[idx]
    delta = value - current
    obj.location[idx] += delta


def bmesh_from_active() -> Tuple[bmesh.types.BMesh, bpy.types.Object]:
    obj = bpy.context.edit_object
    if not obj or obj.type != "MESH":
        raise RuntimeError("Active edit object must be a Mesh")
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    return bm, obj


def selected_vert_world_coords(bm: bmesh.types.BMesh, obj: bpy.types.Object) -> List[Vector]:
    mw = obj.matrix_world
    return [mw @ v.co for v in bm.verts if v.select]


def set_selected_verts_axis(bm: bmesh.types.BMesh, obj: bpy.types.Object, axis: str, target: float) -> None:
    idx = axis_index(axis)
    mw = obj.matrix_world
    imw = mw.inverted_safe()
    for v in bm.verts:
        if not v.select:
            continue
        w = mw @ v.co
        w[idx] = target
        v.co = imw @ w


def bounds_of_selected_verts_world(bm: bmesh.types.BMesh, obj: bpy.types.Object) -> Tuple[Vector, Vector]:
    coords = selected_vert_world_coords(bm, obj)
    if not coords:
        zero = Vector((0.0, 0.0, 0.0))
        return zero, zero
    min_v = Vector((min(v.x for v in coords), min(v.y for v in coords), min(v.z for v in coords)))
    max_v = Vector((max(v.x for v in coords), max(v.y for v in coords), max(v.z for v in coords)))
    return min_v, max_v


def mirror_point_across_plane(point: Vector, axis: str, origin: Vector) -> Vector:
    idx = axis_index(axis)
    mirrored = point.copy()
    mirrored[idx] = 2.0 * origin[idx] - mirrored[idx]
    return mirrored


def sort_objects_by_axis(objs: List[bpy.types.Object], axis: str) -> List[bpy.types.Object]:
    idx = axis_index(axis)
    return sorted(objs, key=lambda o: (o.matrix_world.translation[idx]))


def scale_object_world_axis(obj: bpy.types.Object, axis: str, factor: float) -> None:
    """Scale object along a world axis while keeping object origin location constant."""
    from mathutils import Matrix

    if factor == 1.0 or factor <= 0.0:
        return
    idx = axis_index(axis)
    axis_vec = Vector((1.0 if idx == 0 else 0.0, 1.0 if idx == 1 else 0.0, 1.0 if idx == 2 else 0.0))
    t_old = obj.matrix_world.translation.copy()
    S = Matrix.Scale(factor, 4, axis_vec)
    new_mw = S @ obj.matrix_world
    new_mw.translation = t_old
    obj.matrix_world = new_mw


def origin_point(context: bpy.types.Context, mode: str, objs: Optional[Sequence[bpy.types.Object]] = None) -> Vector:
    mode = mode.upper()
    if mode == "WORLD":
        return Vector((0.0, 0.0, 0.0))
    if mode == "CURSOR":
        return context.scene.cursor.location.copy()
    if mode == "ACTIVE":
        obj = context.view_layer.objects.active
        return obj.matrix_world.translation.copy() if obj else Vector((0.0, 0.0, 0.0))
    # SELECTION
    if objs is None:
        objs = selected_objects(context)
    if not objs:
        return Vector((0.0, 0.0, 0.0))
    mn, mx = world_bounds_of_objects(objs)
    return 0.5 * (mn + mx)


def plane_axes_from_normal(normal_axis: str) -> Tuple[int, int, int]:
    """Return (plane_axis_a, plane_axis_b, normal_axis_index) for a circle plane given normal axis."""
    normal_axis = normal_axis.upper()
    if normal_axis == "Z":
        return 0, 1, 2  # XY plane, normal Z
    if normal_axis == "Y":
        return 0, 2, 1  # XZ plane, normal Y
    return 1, 2, 0  # YZ plane, normal X


def radians(angle_degrees: float) -> float:
    return math.radians(angle_degrees)


