from typing import List

import bpy

from .utils import AXES, world_bounds_of_object


class ALIGNMENT_SUITE_OT_space_inside(bpy.types.Operator):
    bl_idname = "alignment_suite.space_inside"
    bl_label = "Space Inside Range"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(items=[(a, a, f"Axis {a}") for a in AXES], name="Axis", default="X")
    range_min: bpy.props.FloatProperty(name="Range Min", default=0.0)
    range_max: bpy.props.FloatProperty(name="Range Max", default=10.0)
    mode: bpy.props.EnumProperty(items=[("CENTER", "Center", "Center-to-center spacing"), ("GAP", "Gap", "Gap between bounds")], default="CENTER")

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and len(context.selected_objects) >= 2

    def execute(self, context):
        objs: List[bpy.types.Object] = sorted(context.selected_objects, key=lambda o: o.matrix_world.translation[{"X":0,"Y":1,"Z":2}[self.axis]])
        idx = {"X": 0, "Y": 1, "Z": 2}[self.axis]
        span = self.range_max - self.range_min
        if span <= 0.0:
            return {"CANCELLED"}

        if self.mode == "CENTER":
            step = span / (len(objs) - 1)
            for i, o in enumerate(objs):
                loc = o.location.copy()
                loc[idx] = self.range_min + i * step
                o.location = loc
        else:
            # GAP mode requires widths
            widths = []
            total_w = 0.0
            for o in objs:
                mn, mx = world_bounds_of_object(o)
                w = mx[idx] - mn[idx]
                widths.append(w)
                total_w += w
            total_gap = span - total_w
            if total_gap < 0.0:
                total_gap = 0.0
            gap = total_gap / (len(objs) - 1)
            cursor = self.range_min
            for i, o in enumerate(objs):
                mn, _ = world_bounds_of_object(o)
                delta = cursor - mn[idx]
                o.location[idx] += delta
                cursor += widths[i] + gap

        return {"FINISHED"}


classes = (
    ALIGNMENT_SUITE_OT_space_inside,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


