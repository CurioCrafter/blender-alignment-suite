from typing import List

import bpy
from mathutils import Vector

from .utils import AXES, active_object, alignment_target_value, mirror_point_across_plane, world_bounds_of_object


class ALIGNMENT_SUITE_OT_mirror_objects(bpy.types.Operator):
    bl_idname = "alignment_suite.mirror_objects"
    bl_label = "Mirror Objects"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(items=[(a, a, f"Mirror across {a}") for a in AXES], name="Axis", default="X")
    plane_origin_mode: bpy.props.EnumProperty(
        items=[
            ("WORLD", "World Origin", "Mirror around world origin"),
            ("CURSOR", "3D Cursor", "Mirror around cursor position"),
            ("ACTIVE", "Active Object Center", "Mirror around active object's center"),
            ("SELECTION", "Selection Bounds Center", "Mirror around selection bounds center"),
        ],
        name="Plane Origin",
        default="WORLD",
    )
    duplicate: bpy.props.BoolProperty(name="Duplicate", default=True, description="If enabled, creates mirrored duplicates instead of transforming originals")

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) >= 1 and context.mode == 'OBJECT'

    def execute(self, context):
        objs: List[bpy.types.Object] = [o for o in context.selected_objects]
        idx = {"X": 0, "Y": 1, "Z": 2}[self.axis]

        # Determine plane origin
        if self.plane_origin_mode in {"WORLD", "CURSOR", "ACTIVE"}:
            origin_value = alignment_target_value(context, self.axis, self.plane_origin_mode)
        else:
            # selection bounds center
            from .utils import world_bounds_of_objects

            mn_all, mx_all = world_bounds_of_objects(objs)
            origin_value = 0.5 * (mn_all[idx] + mx_all[idx])

        for obj in objs:
            if self.duplicate:
                new_obj = obj.copy()
                new_obj.data = obj.data.copy() if obj.data else None
                context.collection.objects.link(new_obj)
                target = new_obj
            else:
                target = obj

            loc = target.location.copy()
            loc[idx] = 2.0 * origin_value - loc[idx]
            target.location = loc

            # Mirror rotation and scale along axis
            scale = list(target.scale)
            scale[idx] *= -1.0
            target.scale = scale

        return {"FINISHED"}


class ALIGNMENT_SUITE_OT_mirror_mesh(bpy.types.Operator):
    bl_idname = "alignment_suite.mirror_mesh"
    bl_label = "Mirror Mesh"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(items=[(a, a, f"Mirror across {a}") for a in AXES], name="Axis", default="X")
    plane_origin_mode: bpy.props.EnumProperty(
        items=[
            ("WORLD", "World Origin", "Mirror around world origin"),
            ("CURSOR", "3D Cursor", "Mirror around cursor position"),
            ("ACTIVE", "Active Object Center", "Mirror around active object's center"),
            ("SELECTION", "Selection Bounds Center", "Mirror around selection bounds center"),
        ],
        name="Plane Origin",
        default="WORLD",
    )
    duplicate: bpy.props.BoolProperty(name="Duplicate", default=False, description="If enabled, duplicate selected elements before mirroring")

    @classmethod
    def poll(cls, context):
        obj = context.edit_object
        return obj is not None and obj.type == 'MESH' and context.mode == 'EDIT_MESH'

    def execute(self, context):
        import bmesh
        from .utils import bmesh_from_active, set_selected_verts_axis

        bm, obj = bmesh_from_active()
        mw = obj.matrix_world
        imw = mw.inverted_safe()
        idx = {"X": 0, "Y": 1, "Z": 2}[self.axis]

        if self.plane_origin_mode in {"WORLD", "CURSOR", "ACTIVE"}:
            origin_value = alignment_target_value(context, self.axis, self.plane_origin_mode)
        else:
            from .utils import bounds_of_selected_verts_world

            mn, mx = bounds_of_selected_verts_world(bm, obj)
            origin_value = 0.5 * (mn[idx] + mx[idx])

        if self.duplicate:
            geom = [v for v in bm.verts if v.select] + [e for e in bm.edges if e.select] + [f for f in bm.faces if f.select]
            ret = bmesh.ops.duplicate(bm, geom=geom)
            new_geom = ret.get("geom", [])
            for elem in new_geom:
                elem.select = True

        for v in bm.verts:
            if not v.select:
                continue
            w = mw @ v.co
            w[idx] = 2.0 * origin_value - w[idx]
            v.co = imw @ w

        bmesh.update_edit_mesh(obj.data)
        return {"FINISHED"}


classes = (
    ALIGNMENT_SUITE_OT_mirror_objects,
    ALIGNMENT_SUITE_OT_mirror_mesh,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


