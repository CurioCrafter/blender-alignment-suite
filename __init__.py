bl_info = {
    "name": "Alignment Suite",
    "author": "CurioCrafter",
    "version": (1, 0, 0),
    "blender": (4, 5, 0),
    "location": "View3D > Sidebar > Align Suite",
    "description": "Comprehensive alignment, distribution, and mirroring tools for objects and meshes",
    "warning": "",
    "doc_url": "https://github.com/CurioCrafter/blender-alignment-suite",
    "category": "3D View",
}

import importlib
import bpy

from . import utils as _utils
from . import ops_align as _ops_align
from . import ops_distribute as _ops_distribute
from . import ops_mirror as _ops_mirror
from . import ops_cursor as _ops_cursor
from . import ops_orient as _ops_orient
from . import ops_snap as _ops_snap
from . import ops_spacing as _ops_spacing
from . import ui as _ui


def reload_modules():
    for m in (_utils, _ops_align, _ops_distribute, _ops_mirror, _ops_cursor, _ops_orient, _ops_snap, _ops_spacing, _ui):
        importlib.reload(m)


class ALIGNMENT_SUITE_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    show_advanced: bpy.props.BoolProperty(
        name="Show Advanced Options",
        default=False,
        description="Expose additional advanced options in the UI",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "show_advanced")

def register():
    bpy.utils.register_class(ALIGNMENT_SUITE_Preferences)
    # Register submodules (they register their own classes and props)
    _ops_align.register()
    _ops_distribute.register()
    _ops_mirror.register()
    _ops_cursor.register()
    _ops_orient.register()
    _ops_snap.register()
    _ops_spacing.register()
    _ui.register()


def unregister():
    # Unregister in reverse order
    _ui.unregister()
    _ops_cursor.unregister()
    _ops_spacing.unregister()
    _ops_snap.unregister()
    _ops_orient.unregister()
    _ops_mirror.unregister()
    _ops_distribute.unregister()
    _ops_align.unregister()
    bpy.utils.unregister_class(ALIGNMENT_SUITE_Preferences)


if __name__ == "__main__":
    register()


