"""Main module."""
from pathlib import Path
import sys

import bpy  # noqa: E0401


# Add current module to path so the Blender interpreter finds it
PARENT_PATH = str(Path(bpy.data.filepath).parent.parent.resolve())
print(PARENT_PATH)
if PARENT_PATH not in sys.path:
    sys.path.append(PARENT_PATH)

from dem3d.cli_utils import ArgumentParserForBlender  # noqa: E402, E0401
from dem3d.render import render_movie  # noqa: E402, E0401

# TODO: Load the blenderGIS addon
#  https://blender.stackexchange.com/questions/8984/how-to-load-an-addon-from-a-python-script
# TODO: Create camera and lights (don't use the default ones since in headless we will not have a blank .blend file)
# TODO: IM SUSPICIOUS that running blender as a py module will give issues with the context or something. Heads up!
from dem3d.scene import make_dem_with_texture  # noqa: E402, E0401


if __name__ == "__main__":

    parser = ArgumentParserForBlender()
    parser.add_argument("--movie", action="store_true", help="Render animation and quit")
    parser.add_argument("-dem", "--dem_path", type=Path, required=True)
    parser.add_argument("-r", "--raster_path", type=Path, required=True)
    parser.add_argument("-p", "--raster_pattern", type=str, required=True, help="Pattern to match raster file names")
    parser.add_argument(
        "-o",
        "--out_file",
        type=Path,
        required="--movie" in sys.argv,
        help="Output location of the rendered animation. Required when --movie is passed",
    )
    parser.add_argument(
        "-fps", "--fps", type=int, default=6, help="movie frames per second. Only used when --movie is passed"
    )
    parser.add_argument("-s", "--strength", type=float, default=1)

    args = parser.parse_args()

    raster_paths = sorted(list(args.raster_path.glob(args.raster_pattern)))
    if args.movie:
        render_movie(args.dem_path, args.raster_path, args.out_file, args.raster_pattern, args.fps, args.strength)
        bpy.ops.wm.quit_blender()  # quit blender to avoid memory issues with the next running of the script.
    else:
        make_dem_with_texture(args.dem_path, raster_paths, args.strength)
