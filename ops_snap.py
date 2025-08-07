from typing import List

import bpy
from mathutils import Vector

from .utils import AXES, world_bounds_of_object


class ALIGNMENT_SUITE_OT_snap_minmax_to_minmax(bpy.types.Operator):
    bl_idname = "alignment_suite.snap_minmax_to_minmax"
    bl_label = "Snap Edge -> Edge"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(items=[(a, a, f"Axis {a}") for a in AXES], name="Axis", default="X")
    source_side: bpy.props.EnumProperty(items=[("MIN", "Min", "Use minimum bound"), ("MAX", "Max", "Use maximum bound")], name="Source Side", default="MIN")
    target_side: bpy.props.EnumProperty(items=[("MIN", "Min", "Use minimum bound"), ("MAX", "Max", "Use maximum bound")], name="Target Side", default="MIN")
    target: bpy.props.EnumProperty(items=[("ACTIVE", "Active", "Use active object as target"), ("CURSOR", "Cursor", "Use 3D Cursor as target"), ("WORLD", "World 0", "Use world origin")], name="Target", default="ACTIVE")

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and len(context.selected_objects) >= 1

    def execute(self, context):
        idx = {"X": 0, "Y": 1, "Z": 2}[self.axis]
        sel = [o for o in context.selected_objects]
        act = context.view_layer.objects.active

        if self.target == "ACTIVE" and act is not None:
            t_mn, t_mx = world_bounds_of_object(act)
            t_val = t_mn[idx] if self.target_side == "MIN" else t_mx[idx]
        elif self.target == "CURSOR":
            t_val = context.scene.cursor.location[idx]
        else:
            t_val = 0.0

        for o in sel:
            if self.target == "ACTIVE" and o == act:
                continue
            s_mn, s_mx = world_bounds_of_object(o)
            s_val = s_mn[idx] if self.source_side == "MIN" else s_mx[idx]
            delta = t_val - s_val
            o.location[idx] += delta
        return {"FINISHED"}


class ALIGNMENT_SUITE_OT_snap_to_increment(bpy.types.Operator):
    bl_idname = "alignment_suite.snap_to_increment"
    bl_label = "Snap To Increment"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(items=[(a, a, f"Axis {a}") for a in AXES], name="Axis", default="X")
    increment: bpy.props.FloatProperty(name="Increment", default=0.1, min=0.0)

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.selected_objects

    def execute(self, context):
        idx = {"X": 0, "Y": 1, "Z": 2}[self.axis]
        inc = self.increment if self.increment > 0.0 else 0.0
        for o in context.selected_objects:
            loc = o.location.copy()
            loc[idx] = round(loc[idx] / inc) * inc if inc > 0.0 else loc[idx]
            o.location = loc
        return {"FINISHED"}


classes = (
    ALIGNMENT_SUITE_OT_snap_minmax_to_minmax,
    ALIGNMENT_SUITE_OT_snap_to_increment,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


