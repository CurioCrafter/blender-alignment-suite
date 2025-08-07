import bpy


class ALIGNMENT_SUITE_PT_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Align Suite'
    bl_label = 'Alignment Suite'

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.label(text="Align Objects")
        row = col.row(align=True)
        for axis in ('X', 'Y', 'Z'):
            op = row.operator('alignment_suite.align_objects', text=f'Align {axis}')
            op.axis = axis
            op.mode = context.scene.alignment_suite_align_mode
            op.use_bounds = context.scene.alignment_suite_use_bounds
            op.which_bound = context.scene.alignment_suite_which_bound
            op.offset = context.scene.alignment_suite_align_offset

        col.separator()
        col.prop(context.scene, 'alignment_suite_align_mode', text='Target')
        col.prop(context.scene, 'alignment_suite_use_bounds', text='Use Bounds')
        if context.scene.alignment_suite_use_bounds:
            col.prop(context.scene, 'alignment_suite_which_bound', text='Bound')

        # Distribute
        col.separator()
        col.label(text="Distribute Objects")
        row = col.row(align=True)
        op = row.operator('alignment_suite.distribute_objects', text='Distribute X')
        op.axis = 'X'
        op.spacing_mode = context.scene.alignment_suite_spacing_mode
        op = row.operator('alignment_suite.distribute_objects', text='Distribute Y')
        op.axis = 'Y'
        op.spacing_mode = context.scene.alignment_suite_spacing_mode
        op = row.operator('alignment_suite.distribute_objects', text='Distribute Z')
        op.axis = 'Z'
        op.spacing_mode = context.scene.alignment_suite_spacing_mode
        col.prop(context.scene, 'alignment_suite_spacing_mode', text='Spacing')

        # Distribute by distance
        col.separator()
        col.label(text="Distribute By Distance")
        row = col.row(align=True)
        for axis in ('X', 'Y', 'Z'):
            op = row.operator('alignment_suite.distribute_by_distance', text=f'{axis}')
            op.axis = axis
            op.distance_mode = context.scene.alignment_suite_distance_mode
            op.distance = context.scene.alignment_suite_distance_value
        row = col.row(align=True)
        col.prop(context.scene, 'alignment_suite_distance_mode', text='Mode')
        col.prop(context.scene, 'alignment_suite_distance_value', text='Distance')

        # Grid
        col.separator()
        col.label(text="Grid Arrange")
        row = col.row(align=True)
        op = row.operator('alignment_suite.distribute_grid', text='Arrange Grid')
        op.primary_axis = context.scene.alignment_suite_grid_primary
        op.secondary_axis = context.scene.alignment_suite_grid_secondary
        op.columns = context.scene.alignment_suite_grid_columns
        op.spacing_primary = context.scene.alignment_suite_grid_spacing_primary
        op.spacing_secondary = context.scene.alignment_suite_grid_spacing_secondary
        op.order_by_axis = context.scene.alignment_suite_grid_sort
        grid = col.box()
        grid.prop(context.scene, 'alignment_suite_grid_primary', text='Primary')
        grid.prop(context.scene, 'alignment_suite_grid_secondary', text='Secondary')
        grid.prop(context.scene, 'alignment_suite_grid_columns', text='Columns')
        grid.prop(context.scene, 'alignment_suite_grid_spacing_primary', text='Primary Spacing')
        grid.prop(context.scene, 'alignment_suite_grid_spacing_secondary', text='Secondary Spacing')
        grid.prop(context.scene, 'alignment_suite_grid_sort', text='Sort By')

        # Mirror
        col.separator()
        col.label(text="Mirror Objects")
        row = col.row(align=True)
        for axis in ('X', 'Y', 'Z'):
            op = row.operator('alignment_suite.mirror_objects', text=f'Mirror {axis}')
            op.axis = axis
            op.plane_origin_mode = context.scene.alignment_suite_plane_origin
            op.duplicate = context.scene.alignment_suite_duplicate_on_mirror

        col.prop(context.scene, 'alignment_suite_plane_origin', text='Plane Origin')
        col.prop(context.scene, 'alignment_suite_duplicate_on_mirror', text='Duplicate')

        # Cursor/Origin
        col.separator()
        col.label(text="Cursor / Origin")
        row = col.row(align=True)
        op = row.operator('alignment_suite.set_cursor', text='Cursor X')
        op.axis = 'X'
        op.mode = context.scene.alignment_suite_cursor_mode
        op = row.operator('alignment_suite.set_cursor', text='Cursor Y')
        op.axis = 'Y'
        op.mode = context.scene.alignment_suite_cursor_mode
        op = row.operator('alignment_suite.set_cursor', text='Cursor Z')
        op.axis = 'Z'
        op.mode = context.scene.alignment_suite_cursor_mode
        col.prop(context.scene, 'alignment_suite_cursor_mode', text='Cursor Mode')

        # Mesh tools (visible in Edit mode too via separate panel)

        # Orientation and Size
        col.separator()
        col.label(text="Orient / Size")
        row = col.row(align=True)
        op = row.operator('alignment_suite.orient_to_point', text='Aim At Target')
        op.local_axis = context.scene.alignment_suite_orient_local
        op.up_axis = context.scene.alignment_suite_orient_up
        op.target_mode = context.scene.alignment_suite_orient_target
        op.invert = context.scene.alignment_suite_orient_invert

        row = col.row(align=True)
        for axis in ('X','Y','Z'):
            op = row.operator('alignment_suite.match_size_axis', text=f'Match {axis}')
            op.axis = axis
            op.size = context.scene.alignment_suite_match_size
            op.uniform = context.scene.alignment_suite_match_uniform

        box = col.box()
        box.prop(context.scene, 'alignment_suite_orient_local', text='Local Axis')
        box.prop(context.scene, 'alignment_suite_orient_up', text='Up')
        box.prop(context.scene, 'alignment_suite_orient_target', text='Target')
        box.prop(context.scene, 'alignment_suite_orient_invert', text='Invert')
        box.prop(context.scene, 'alignment_suite_match_size', text='Size')
        box.prop(context.scene, 'alignment_suite_match_uniform', text='Uniform')

        # Snapping & Spacing
        col.separator()
        col.label(text="Snap / Space")
        row = col.row(align=True)
        for axis in ('X','Y','Z'):
            op = row.operator('alignment_suite.snap_minmax_to_minmax', text=f'Snap {axis}')
            op.axis = axis
            op.source_side = context.scene.alignment_suite_snap_source
            op.target_side = context.scene.alignment_suite_snap_target_side
            op.target = context.scene.alignment_suite_snap_target
        grid = col.box()
        grid.prop(context.scene, 'alignment_suite_snap_source', text='Source Side')
        grid.prop(context.scene, 'alignment_suite_snap_target_side', text='Target Side')
        grid.prop(context.scene, 'alignment_suite_snap_target', text='Target')

        row = col.row(align=True)
        for axis in ('X','Y','Z'):
            op = row.operator('alignment_suite.snap_to_increment', text=f'Round {axis}')
            op.axis = axis
            op.increment = context.scene.alignment_suite_snap_increment
        col.prop(context.scene, 'alignment_suite_snap_increment', text='Increment')

        col.separator()
        col.label(text='Space Inside Range')
        row = col.row(align=True)
        for axis in ('X','Y','Z'):
            op = row.operator('alignment_suite.space_inside', text=f'{axis}')
            op.axis = axis
            op.range_min = context.scene.alignment_suite_space_min
            op.range_max = context.scene.alignment_suite_space_max
            op.mode = context.scene.alignment_suite_space_mode
        box2 = col.box()
        box2.prop(context.scene, 'alignment_suite_space_min', text='Min')
        box2.prop(context.scene, 'alignment_suite_space_max', text='Max')
        box2.prop(context.scene, 'alignment_suite_space_mode', text='Mode')


def _update_align_operator_props(self, context):
    # No op: props are read when button pressed; keep for future live UI updates
    pass


def register():
    bpy.utils.register_class(ALIGNMENT_SUITE_PT_panel)

    # Scene props for UI state
    bpy.types.Scene.alignment_suite_align_mode = bpy.props.EnumProperty(
        items=[
            ("WORLD", "World 0", "World origin"),
            ("MIN", "Min", "Selection minimum"),
            ("CENTER", "Center", "Selection center"),
            ("MAX", "Max", "Selection maximum"),
            ("CURSOR", "3D Cursor", "Cursor position"),
            ("ACTIVE", "Active", "Active object center"),
        ],
        name="Align Target",
        default="CENTER",
        update=_update_align_operator_props,
    )
    bpy.types.Scene.alignment_suite_use_bounds = bpy.props.BoolProperty(name="Use Bounds", default=False, update=_update_align_operator_props)
    bpy.types.Scene.alignment_suite_which_bound = bpy.props.EnumProperty(items=[("MIN", "Min", ""), ("CENTER", "Center", ""), ("MAX", "Max", "")], default="CENTER")
    bpy.types.Scene.alignment_suite_align_offset = bpy.props.FloatProperty(name="Offset", default=0.0)
    bpy.types.Scene.alignment_suite_spacing_mode = bpy.props.EnumProperty(items=[("GAP", "Equal Gap", ""), ("CENTER", "Equal Center", "")], default="GAP")
    bpy.types.Scene.alignment_suite_distance_mode = bpy.props.EnumProperty(items=[("CENTER", "Center Distance", ""), ("GAP", "Gap Distance", "")], default="CENTER")
    bpy.types.Scene.alignment_suite_distance_value = bpy.props.FloatProperty(name="Distance", default=1.0, min=0.0)
    bpy.types.Scene.alignment_suite_plane_origin = bpy.props.EnumProperty(items=[("WORLD", "World", ""), ("CURSOR", "Cursor", ""), ("ACTIVE", "Active", ""), ("SELECTION", "Selection", "")], default="WORLD")
    bpy.types.Scene.alignment_suite_duplicate_on_mirror = bpy.props.BoolProperty(name="Duplicate on Mirror", default=True)
    bpy.types.Scene.alignment_suite_cursor_mode = bpy.props.EnumProperty(items=[("WORLD", "World 0", ""), ("MIN", "Min", ""), ("CENTER", "Center", ""), ("MAX", "Max", ""), ("ACTIVE", "Active", "")], default="CENTER")

    # Grid props
    bpy.types.Scene.alignment_suite_grid_primary = bpy.props.EnumProperty(items=[('X','X',''),('Y','Y',''),('Z','Z','')], default='X')
    bpy.types.Scene.alignment_suite_grid_secondary = bpy.props.EnumProperty(items=[('X','X',''),('Y','Y',''),('Z','Z','')], default='Y')
    bpy.types.Scene.alignment_suite_grid_columns = bpy.props.IntProperty(name="Columns", default=3, min=1)
    bpy.types.Scene.alignment_suite_grid_spacing_primary = bpy.props.FloatProperty(name="Primary Spacing", default=1.0, min=0.0)
    bpy.types.Scene.alignment_suite_grid_spacing_secondary = bpy.props.FloatProperty(name="Secondary Spacing", default=1.0, min=0.0)
    bpy.types.Scene.alignment_suite_grid_sort = bpy.props.EnumProperty(items=[('X','X',''),('Y','Y',''),('Z','Z','')], default='X')

    # Orient/Size props
    bpy.types.Scene.alignment_suite_orient_local = bpy.props.EnumProperty(items=[('X','X',''),('Y','Y',''),('Z','Z','')], default='Y')
    bpy.types.Scene.alignment_suite_orient_up = bpy.props.EnumProperty(items=[('X','X',''),('Y','Y',''),('Z','Z','')], default='Z')
    bpy.types.Scene.alignment_suite_orient_target = bpy.props.EnumProperty(items=[('WORLD','World',''),('CURSOR','Cursor',''),('ACTIVE','Active',''),('SELECTION','Selection','')], default='SELECTION')
    bpy.types.Scene.alignment_suite_orient_invert = bpy.props.BoolProperty(name='Invert Aim', default=False)
    bpy.types.Scene.alignment_suite_match_size = bpy.props.FloatProperty(name='Match Size', default=1.0, min=0.0)
    bpy.types.Scene.alignment_suite_match_uniform = bpy.props.BoolProperty(name='Uniform', default=False)

    # Snap/Space props
    bpy.types.Scene.alignment_suite_snap_source = bpy.props.EnumProperty(items=[('MIN','Min',''),('MAX','Max','')], default='MIN')
    bpy.types.Scene.alignment_suite_snap_target_side = bpy.props.EnumProperty(items=[('MIN','Min',''),('MAX','Max','')], default='MIN')
    bpy.types.Scene.alignment_suite_snap_target = bpy.props.EnumProperty(items=[('ACTIVE','Active',''),('CURSOR','Cursor',''),('WORLD','World 0','')], default='ACTIVE')
    bpy.types.Scene.alignment_suite_snap_increment = bpy.props.FloatProperty(name='Increment', default=0.1, min=0.0)
    bpy.types.Scene.alignment_suite_space_min = bpy.props.FloatProperty(name='Range Min', default=0.0)
    bpy.types.Scene.alignment_suite_space_max = bpy.props.FloatProperty(name='Range Max', default=10.0)
    bpy.types.Scene.alignment_suite_space_mode = bpy.props.EnumProperty(items=[('CENTER','Center',''),('GAP','Gap','')], default='CENTER')


def unregister():
    del bpy.types.Scene.alignment_suite_align_mode
    del bpy.types.Scene.alignment_suite_use_bounds
    del bpy.types.Scene.alignment_suite_which_bound
    del bpy.types.Scene.alignment_suite_align_offset
    del bpy.types.Scene.alignment_suite_spacing_mode
    del bpy.types.Scene.alignment_suite_distance_mode
    del bpy.types.Scene.alignment_suite_distance_value
    del bpy.types.Scene.alignment_suite_plane_origin
    del bpy.types.Scene.alignment_suite_duplicate_on_mirror
    del bpy.types.Scene.alignment_suite_cursor_mode
    del bpy.types.Scene.alignment_suite_grid_primary
    del bpy.types.Scene.alignment_suite_grid_secondary
    del bpy.types.Scene.alignment_suite_grid_columns
    del bpy.types.Scene.alignment_suite_grid_spacing_primary
    del bpy.types.Scene.alignment_suite_grid_spacing_secondary
    del bpy.types.Scene.alignment_suite_grid_sort

    del bpy.types.Scene.alignment_suite_orient_local
    del bpy.types.Scene.alignment_suite_orient_up
    del bpy.types.Scene.alignment_suite_orient_target
    del bpy.types.Scene.alignment_suite_orient_invert
    del bpy.types.Scene.alignment_suite_match_size
    del bpy.types.Scene.alignment_suite_match_uniform

    del bpy.types.Scene.alignment_suite_snap_source
    del bpy.types.Scene.alignment_suite_snap_target_side
    del bpy.types.Scene.alignment_suite_snap_target
    del bpy.types.Scene.alignment_suite_snap_increment
    del bpy.types.Scene.alignment_suite_space_min
    del bpy.types.Scene.alignment_suite_space_max
    del bpy.types.Scene.alignment_suite_space_mode
    bpy.utils.unregister_class(ALIGNMENT_SUITE_PT_panel)


