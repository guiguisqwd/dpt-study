"""Open the pinned Z-Anatomy .blend with scripts disabled, then run the vendored exporter.

Called by build-addon.py in a Python that can `import bpy` (pip install bpy==5.2.0):
    python run_export.py -- <Startup.blend> <export_batch.py> --config C --batch B --output DIR
"""
import runpy
import sys

import bpy

argv = sys.argv[sys.argv.index('--') + 1:]
blend, exporter, rest = argv[0], argv[1], argv[2:]
bpy.ops.wm.open_mainfile(filepath=blend, load_ui=False, use_scripts=False)
sys.argv = ['blender', '--'] + rest
runpy.run_path(exporter, run_name='__main__')
