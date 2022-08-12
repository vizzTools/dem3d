"""Script to render a movie from a DEM and a set of rasters."""
from pathlib import Path
import sys

import bpy  # noqa: E0401


# Add current module to path so the Blender interpreter finds it
PARENT_PATH = str(Path(bpy.data.filepath).parent.parent.resolve())
if PARENT_PATH not in sys.path:
    sys.path.append(PARENT_PATH)

from dem3d.scene import make_dem_with_texture


def render_movie(dem_path: Path, raster_path: Path, out_file: Path, pattern: str, fps: int, strength: float):
    """Render the current animation of the active scene."""
    rasters = sorted(list(raster_path.glob(pattern)))
    make_dem_with_texture(dem_path, rasters, strength)

    # Render frames
    scene = bpy.context.scene
    scene.frame_start = 0
    scene.frame_end = len(rasters)

    # Render settings
    render = scene.render
    render.resolution_x = 1920 * 2
    render.resolution_y = 1080 * 2
    render.image_settings.file_format = "FFMPEG"  # needs to be set for the video to be created
    render.fps = fps

    # FFMPEG settings
    render.ffmpeg.codec = "MPEG4"
    render.ffmpeg.constant_rate_factor = "PERC_LOSSLESS"
    render.ffmpeg.format = "MPEG4"

    render.filepath = str(out_file)
    bpy.ops.render.render(animation=True)
