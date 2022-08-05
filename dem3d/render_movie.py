"""Script to render a movie from a DEM and a set of rasters."""
from pathlib import Path
import sys

import bpy  # noqa: E0401


PARENT_PATH = str(Path(bpy.data.filepath).parent.parent.resolve())
if PARENT_PATH not in sys.path:
    sys.path.append(PARENT_PATH)

from cli_utils import ArgumentParserForBlender  # noqa: E402, E0401

from dem3d import make_dem_with_texture  # noqa: E402, E0401, E0611


def main(dem_path: Path, raster_path: Path, out_file: Path, pattern: str, fps: int, strength: float):  # noqa: D103
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


if __name__ == "__main__":
    parser = ArgumentParserForBlender()
    parser.add_argument("-dem", "--dem_path", type=Path, required=True)
    parser.add_argument("-r", "--raster_path", type=Path, required=True)
    parser.add_argument("-o", "--out_file", type=Path, required=True)
    parser.add_argument("-p", "--raster_pattern", type=str, required=True, help="Pattern to match raster file names")
    parser.add_argument("-fps", "--fps", type=int, default=6)
    parser.add_argument("-s", "--strength", type=float, default=1)
    args = parser.parse_args()

    main(args.dem_path, args.raster_path, args.out_file, args.raster_pattern, args.fps, args.strength)
    bpy.ops.wm.quit_blender()  # quit blender to avoid memory issues with the next running of the script.
