
dem3d
=====

Create blender scenes, render movies from dem and raster timeseries


## Usage

Use vizzDL to generate time series rasters and DEMs, as done in https://github.com/Vizzuality/redes-data/blob/main/notebooks/Lab/12_3D_Terrain.ipynb

Then use this script to create an animated blender scene (start the animation with the space bar):

```shell
   blender -P dem3d/dem3d.py -- --dem_path Barcelona/elevation.3857.tif --raster_path Barcelona --raster_pattern "RGB.*.tif" --strength 2.5
```

Note that (for now) the script must be run from Blender's Python (by using the `-P` flag). Also, since blender command accepts arguments, the python arguments must be placed after the `--` flag.

In order to render a movie use:

```shell
blender -b -P render_movie.py -- -dem Barcelona/elevation.3857.tif -r Barcelona -o renders/barcelona.mp4 -p "RGB.*.tif" -fps 4 -s 2.5
```

## TODO

- [ ] Build or find a way to use blender as a python module
- [ ] Improve camera settings to adapt to different scene sizes
- [ ] Download and install blenderGIS addon automatically
- [ ] Export scene as glTF
- [ ] Animate glTF or discuss with frontend team best way to do this.
