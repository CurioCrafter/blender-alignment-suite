import bpy

from .utils import AXES, alignment_target_value


class ALIGNMENT_SUITE_OT_set_cursor(bpy.types.Operator):
    bl_idname = "alignment_suite.set_cursor"
    bl_label = "Set 3D Cursor"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(items=[(a, a, f"Axis {a}") for a in AXES], name="Axis", default="X")
    mode: bpy.props.EnumProperty(
        items=[
            ("WORLD", "World 0", "World origin"),
            ("MIN", "Selection Min", "Selection minimum bound"),
            ("CENTER", "Selection Center", "Selection bounds center"),
            ("MAX", "Selection Max", "Selection maximum bound"),
            ("ACTIVE", "Active Center", "Active object center"),
        ],
        name="Mode",
        default="CENTER",
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and (context.selected_objects or context.view_layer.objects.active)

    def execute(self, context):
        idx = {"X": 0, "Y": 1, "Z": 2}[self.axis]
        target_value = alignment_target_value(context, self.axis, self.mode)
        cur = context.scene.cursor.location.copy()
        cur[idx] = target_value
        context.scene.cursor.location = cur
        return {"FINISHED"}


class ALIGNMENT_SUITE_OT_origin_to_cursor_axis(bpy.types.Operator):
    bl_idname = "alignment_suite.origin_to_cursor_axis"
    bl_label = "Origin -> Cursor (Axis)"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(items=[(a, a, f"Axis {a}") for a in AXES], name="Axis", default="X")

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.selected_objects

    def execute(self, context):
        idx = {"X": 0, "Y": 1, "Z": 2}[self.axis]
        target = context.scene.cursor.location[idx]
        for obj in context.selected_objects:
            loc = obj.location.copy()
            loc[idx] = target
            obj.location = loc
        return {"FINISHED"}


classes = (
    ALIGNMENT_SUITE_OT_set_cursor,
    ALIGNMENT_SUITE_OT_origin_to_cursor_axis,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


