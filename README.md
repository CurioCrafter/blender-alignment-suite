Alignment Suite (Blender 4.5)
================================

Comprehensive alignment, distribution, mirroring, and cursor/origin tools for Blender 4.5.

Features
- Align objects along X/Y/Z to: World(0), Selection Min/Center/Max, 3D Cursor, Active object
- Align active to selection bounds
- Align mesh vertices in Edit Mode to the same targets
- Distribute objects with Equal Gap (bounds) or Equal Center spacing
- Mirror objects or selected mesh across X/Y/Z using World/Cursor/Active/Selection plane origin; optional duplicate
- Cursor and Origin helpers: set cursor per-axis to common targets, move object origins along an axis to cursor
- One-panel UI in View3D > Sidebar > Align Suite

Installation
1. In Blender 4.5, go to Edit > Preferences > Add-ons
2. Click Install..., then select a zip containing the `alignment_suite` folder:
   - Zip the `alignment_suite` folder itself, not its parent. The zip root must contain `__init__.py`.
3. Enable the add-on: search for "Alignment Suite"
4. Open 3D Viewport, Sidebar (N), tab "Align Suite"

Usage Highlights
- Set target for alignment in the panel, then press Align X/Y/Z.
- Use "Use Bounds" and choose Min/Center/Max to align by bounds instead of origins.
- Distribute requires 3+ objects; Equal Gap preserves sizes and equalizes gaps.
- Mirror can duplicate or mirror in-place. Choose plane origin in the panel.
- In Edit Mode, use the operators (F3) "Align Verts" and "Mirror Mesh".

Notes
- Works with most object types. For non-mesh types without geometry, bounds fall back to object origin.
- Parented/Constrained objects: complex constraints may affect results; operators work in object transforms space.
- All operators are undoable.


