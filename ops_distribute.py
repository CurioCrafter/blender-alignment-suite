from typing import List

import bpy

from .utils import AXES, sort_objects_by_axis, world_bounds_of_object


class ALIGNMENT_SUITE_OT_distribute_objects(bpy.types.Operator):
    bl_idname = "alignment_suite.distribute_objects"
    bl_label = "Distribute Objects"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(items=[(a, a, f"Distribute along {a}") for a in AXES], name="Axis", default="X")
    spacing_mode: bpy.props.EnumProperty(
        items=[
            ("GAP", "Equal Gap (Bounds)", "Equalize gaps using bounding boxes"),
            ("CENTER", "Equal Center", "Equalize center-to-center distances"),
        ],
        name="Spacing",
        default="GAP",
    )

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) >= 3 and context.mode == 'OBJECT'

    def execute(self, context):
        objs: List[bpy.types.Object] = [o for o in context.selected_objects]
        idx = {"X": 0, "Y": 1, "Z": 2}[self.axis]
        objs = sort_objects_by_axis(objs, self.axis)

        first = objs[0]
        last = objs[-1]

        if self.spacing_mode == "CENTER":
            start = first.matrix_world.translation[idx]
            end = last.matrix_world.translation[idx]
            step = (end - start) / (len(objs) - 1)
            for i, obj in enumerate(objs):
                loc = obj.location.copy()
                loc[idx] = start + step * i
                obj.location = loc
        else:
            # Equal gap using bounds
            fmn, fmx = world_bounds_of_object(first)
            lmn, lmx = world_bounds_of_object(last)
            start = fmn[idx]
            end = lmx[idx]

            total_len = 0.0
            widths = []
            for o in objs:
                mn, mx = world_bounds_of_object(o)
                w = mx[idx] - mn[idx]
                widths.append(w)
                total_len += w
            total_span = end - start
            total_gap = total_span - total_len
            gap = total_gap / (len(objs) - 1)

            cursor = start
            for i, o in enumerate(objs):
                mn, mx = world_bounds_of_object(o)
                w = widths[i]
                # move so that current min == cursor
                delta = cursor - mn[idx]
                o.location[idx] += delta
                cursor += w + gap

        return {"FINISHED"}


class ALIGNMENT_SUITE_OT_distribute_by_distance(bpy.types.Operator):
    bl_idname = "alignment_suite.distribute_by_distance"
    bl_label = "Distribute By Distance"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(items=[(a, a, f"Distribute along {a}") for a in AXES], name="Axis", default="X")
    distance_mode: bpy.props.EnumProperty(
        items=[
            ("CENTER", "Center Distance", "Equalize center-to-center spacing by a given distance"),
            ("GAP", "Gap Distance", "Equalize gap between bounds by a given distance"),
        ],
        name="Mode",
        default="CENTER",
    )
    distance: bpy.props.FloatProperty(name="Distance", default=1.0, min=0.0)

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) >= 2 and context.mode == 'OBJECT'

    def execute(self, context):
        objs: List[bpy.types.Object] = [o for o in context.selected_objects]
        idx = {"X": 0, "Y": 1, "Z": 2}[self.axis]
        objs = sort_objects_by_axis(objs, self.axis)

        if self.distance_mode == "CENTER":
            start_center = objs[0].matrix_world.translation[idx]
            for i, obj in enumerate(objs):
                loc = obj.location.copy()
                loc[idx] = start_center + self.distance * i
                obj.location = loc
        else:
            # GAP mode uses object bounds; maintain first object's min bound, then place others with fixed gap
            # Precompute widths on axis
            widths = []
            for o in objs:
                mn, mx = world_bounds_of_object(o)
                widths.append(mx[idx] - mn[idx])
            first_min = world_bounds_of_object(objs[0])[0][idx]
            cursor = first_min
            for i, o in enumerate(objs):
                w = widths[i]
                # place so that min == cursor
                mn, _ = world_bounds_of_object(o)
                delta = cursor - mn[idx]
                o.location[idx] += delta
                cursor += w + self.distance

        return {"FINISHED"}


class ALIGNMENT_SUITE_OT_distribute_grid(bpy.types.Operator):
    bl_idname = "alignment_suite.distribute_grid"
    bl_label = "Distribute Grid"
    bl_options = {"REGISTER", "UNDO"}

    primary_axis: bpy.props.EnumProperty(items=[(a, a, f"Primary {a}") for a in AXES], name="Primary Axis", default="X")
    secondary_axis: bpy.props.EnumProperty(items=[(a, a, f"Secondary {a}") for a in AXES], name="Secondary Axis", default="Y")
    columns: bpy.props.IntProperty(name="Columns", default=3, min=1)
    spacing_primary: bpy.props.FloatProperty(name="Primary Spacing", default=1.0, min=0.0)
    spacing_secondary: bpy.props.FloatProperty(name="Secondary Spacing", default=1.0, min=0.0)
    order_by_axis: bpy.props.EnumProperty(items=[(a, a, f"Sort by {a}") for a in AXES], name="Order By", default="X")

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) >= 2 and context.mode == 'OBJECT'

    def execute(self, context):
        objs: List[bpy.types.Object] = [o for o in context.selected_objects]
        # Order selection to make grid stable
        objs = sort_objects_by_axis(objs, self.order_by_axis)

        pi = {"X": 0, "Y": 1, "Z": 2}[self.primary_axis]
        si = {"X": 0, "Y": 1, "Z": 2}[self.secondary_axis]

        # Use first object's position as origin
        origin_primary = objs[0].location[pi]
        origin_secondary = objs[0].location[si]

        for idx_obj, obj in enumerate(objs):
            row = idx_obj // self.columns
            col = idx_obj % self.columns
            loc = obj.location.copy()
            loc[pi] = origin_primary + col * self.spacing_primary
            loc[si] = origin_secondary + row * self.spacing_secondary
            obj.location = loc

        return {"FINISHED"}


classes = (
    ALIGNMENT_SUITE_OT_distribute_objects,
    ALIGNMENT_SUITE_OT_distribute_by_distance,
    ALIGNMENT_SUITE_OT_distribute_grid,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


