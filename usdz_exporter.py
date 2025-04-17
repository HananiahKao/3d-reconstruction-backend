import os
import subprocess
import uuid

def export_usdz(mesh_path, output_dir):
    """
    Exports a given mesh (PLY/OBJ) to USDZ using Blender on Linux/macOS.
    Requires Blender >= 3.6 with USD export enabled.
    """
    usdz_filename = f"{uuid.uuid4()}.usdz"
    usdz_path = os.path.join(output_dir, usdz_filename)

    # Specify the full path to Blender's executable (macOS example, change for your OS)
    blender_executable = "/Applications/Blender.app/Contents/MacOS/Blender"  # macOS Blender path (Homebrew installed)
    # blender_executable = "/usr/local/bin/blender"  # Uncomment if using Homebrew on Linux (ensure this is correct)

    blender_script = os.path.join(output_dir, "blender_export_usdz.py")

    # Generate Blender script dynamically
    with open(blender_script, "w") as f:
        f.write(f"""
import bpy
import sys

# Clear existing scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Import the mesh
bpy.ops.import_mesh.ply(filepath=r"{mesh_path}")

# Set the export path
output_path = r"{usdz_path}"

# Export to USD (not USDZ, Blender 3.6+ required for full support)
bpy.ops.wm.usd_export(filepath=output_path, export_usdz=True)

# Quit Blender
bpy.ops.wm.quit_blender()
""")

    # Run Blender with full executable path in background mode
    result = subprocess.run([
        blender_executable, "--background", "--python", blender_script
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        raise RuntimeError("Blender export failed:\n" + result.stderr.decode())

    return usdz_path
