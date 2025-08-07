from typing import List

import bpy
from mathutils import Vector

from .utils import AXES, origin_point


class ALIGNMENT_SUITE_OT_orient_to_point(bpy.types.Operator):
    bl_idname = "alignment_suite.orient_to_point"
    bl_label = "Aim At Target"
    bl_options = {"REGISTER", "UNDO"}

    local_axis: bpy.props.EnumProperty(items=[(a, a, f"Track local {a}") for a in AXES], name="Local Axis", default="Y")
    up_axis: bpy.props.EnumProperty(items=[(a, a, f"Up {a}") for a in AXES], name="Up", default="Z")
    target_mode: bpy.props.EnumProperty(
        items=[
            ("WORLD", "World Origin", "Aim at world origin"),
            ("CURSOR", "3D Cursor", "Aim at cursor position"),
            ("ACTIVE", "Active Object", "Aim at active object location"),
            ("SELECTION", "Selection Center", "Aim at selection center"),
        ],
        name="Target",
        default="SELECTION",
    )
    invert: bpy.props.BoolProperty(name="Invert Direction", default=False)

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.selected_objects

    def execute(self, context):
        target = origin_point(context, self.target_mode)

        track = self.local_axis
        up = self.up_axis

        for obj in context.selected_objects:
            direction = target - obj.matrix_world.translation
            if self.invert:
                direction = -direction
            if direction.length_squared == 0.0:
                continue
            quat = direction.normalized().to_track_quat(track, up)
            prev_mode = obj.rotation_mode
            obj.rotation_mode = 'QUAT'
            obj.rotation_quaternion = quat
            obj.rotation_mode = prev_mode
        return {"FINISHED"}


class ALIGNMENT_SUITE_OT_match_size_axis(bpy.types.Operator):
    bl_idname = "alignment_suite.match_size_axis"
    bl_label = "Match Size (Axis)"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(items=[(a, a, f"Axis {a}") for a in AXES], name="Axis", default="X")
    size: bpy.props.FloatProperty(name="Size", default=1.0, min=0.0)
    uniform: bpy.props.BoolProperty(name="Uniform Scale", default=False, description="Scale uniformly to match the size along axis")

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.selected_objects

    def execute(self, context):
        idx = {"X": 0, "Y": 1, "Z": 2}[self.axis]
        for obj in context.selected_objects:
            dims = obj.dimensions.copy()
            if dims[idx] <= 0.0:
                continue
            factor = self.size / dims[idx]
            if self.uniform:
                obj.scale *= factor
            else:
                sc = list(obj.scale)
                sc[idx] *= factor
                obj.scale = sc
        return {"FINISHED"}


classes = (
    ALIGNMENT_SUITE_OT_orient_to_point,
    ALIGNMENT_SUITE_OT_match_size_axis,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


