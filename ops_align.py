from typing import List

import bpy

from .utils import (
    AXES,
    active_object,
    alignment_target_value,
    bmesh_from_active,
    bounds_of_selected_verts_world,
    origin_point,
    selected_objects,
    set_object_world_location_axis,
)


ALIGN_MODES = [
    ("WORLD", "World 0", "Align to world origin along axis"),
    ("MIN", "Min", "Align to minimum bound"),
    ("CENTER", "Center", "Align to center/median of bounds"),
    ("MAX", "Max", "Align to maximum bound"),
    ("CURSOR", "3D Cursor", "Align to 3D Cursor position"),
    ("ACTIVE", "Active", "Align to active object's bound center"),
]


class ALIGNMENT_SUITE_OT_align_objects(bpy.types.Operator):
    bl_idname = "alignment_suite.align_objects"
    bl_label = "Align Objects"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(items=[(a, a, f"Align along {a}") for a in AXES], name="Axis", default="X")
    mode: bpy.props.EnumProperty(items=ALIGN_MODES, name="Target", default="CENTER")
    use_bounds: bpy.props.BoolProperty(
        name="Use Bounds",
        description="Align object bounds instead of object origin",
        default=False,
    )
    offset: bpy.props.FloatProperty(name="Offset", default=0.0, description="Add an offset to the computed target value")
    which_bound: bpy.props.EnumProperty(
        items=[("MIN", "Min", "Use minimum bound"), ("CENTER", "Center", "Use center of bounds"), ("MAX", "Max", "Use maximum bound")],
        name="Bound",
        default="CENTER",
    )

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) >= 1 and context.mode == 'OBJECT'

    def execute(self, context):
        objs: List[bpy.types.Object] = selected_objects(context)
        if not objs:
            return {"CANCELLED"}

        target_value = alignment_target_value(context, self.axis, self.mode, objs) + self.offset

        for obj in objs:
            set_object_world_location_axis(obj, self.axis, target_value, self.use_bounds, self.which_bound)

        return {"FINISHED"}


class ALIGNMENT_SUITE_OT_align_active_to_selection(bpy.types.Operator):
    bl_idname = "alignment_suite.align_active_to_selection"
    bl_label = "Align Active To Selection"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(items=[(a, a, f"Align along {a}") for a in AXES], name="Axis", default="X")
    which_bound: bpy.props.EnumProperty(
        items=[("MIN", "Min", "Use minimum bound"), ("CENTER", "Center", "Use center of bounds"), ("MAX", "Max", "Use maximum bound")],
        name="Bound",
        default="CENTER",
    )

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) >= 2 and context.mode == 'OBJECT'

    def execute(self, context):
        objs = selected_objects(context)
        act = active_object(context)
        if not act or not objs:
            return {"CANCELLED"}
        target_value = alignment_target_value(context, self.axis, "CENTER", objs)
        set_object_world_location_axis(act, self.axis, target_value, True, self.which_bound)
        return {"FINISHED"}


class ALIGNMENT_SUITE_OT_align_mesh_verts(bpy.types.Operator):
    bl_idname = "alignment_suite.align_mesh_verts"
    bl_label = "Align Verts"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(items=[(a, a, f"Align along {a}") for a in AXES], name="Axis", default="X")
    mode: bpy.props.EnumProperty(items=ALIGN_MODES, name="Target", default="CENTER")

    @classmethod
    def poll(cls, context):
        obj = context.edit_object
        return obj is not None and obj.type == 'MESH' and context.mode == 'EDIT_MESH'

    def execute(self, context):
        import bmesh
        from .utils import set_selected_verts_axis

        bm, obj = bmesh_from_active()
        if not any(v.select for v in bm.verts):
            return {"CANCELLED"}

        # Compute target
        if self.mode in {"WORLD", "CURSOR"}:
            target_value = alignment_target_value(context, self.axis, self.mode)
        elif self.mode == "ACTIVE":
            # Active object's bound center
            target_value = alignment_target_value(context, self.axis, "ACTIVE")
        else:
            # Bounds of selection
            mn, mx = bounds_of_selected_verts_world(bm, obj)
            idx = {"X": 0, "Y": 1, "Z": 2}[self.axis]
            if self.mode == "MIN":
                target_value = mn[idx]
            elif self.mode == "MAX":
                target_value = mx[idx]
            else:
                target_value = 0.5 * (mn[idx] + mx[idx])

        set_selected_verts_axis(bm, obj, self.axis, target_value)
        bmesh.update_edit_mesh(obj.data)

        return {"FINISHED"}


classes = (
    ALIGNMENT_SUITE_OT_align_objects,
    ALIGNMENT_SUITE_OT_align_active_to_selection,
    ALIGNMENT_SUITE_OT_align_mesh_verts,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


