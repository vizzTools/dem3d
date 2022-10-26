Redes
==============================

![](./assets/redes.png)
[Red.es](https://www.red.es/es) is a grant from the Ministerio De Asuntos Económicos Y Transformación Digital to carry out innovation in Vizzuality’s portfolio of Digital Content products and services.

# dem3d

Create blender scenes, render movies from dem and raster timeseries

## Usage

Use vizzDL to generate time series rasters and DEMs, as done in <https://github.com/Vizzuality/redes-data/blob/main/notebooks/Lab/12_3D_Terrain.ipynb>

Then use this script to create an animated blender scene (in blender, start the animation with the space bar):

```shell
   blender -P dem3d.py -- --dem_path Barcelona/elevation.3857.tif --raster_path Barcelona --raster_pattern "RGB.*.tif" --strength 2.5
```

Note that (for now) the script must be run from Blender's Python (by using the `-P` flag). Also, note that since blender command accepts arguments, the python arguments must be placed after the `--` flag.

In order to render a movie use:

```shell
blender -b -P dem3d.py -- --movie -dem Barcelona/elevation.3857.tif -r Barcelona -o renders/barcelona.mp4 -p "RGB.*.tif" -fps 4 -s 2.5
```

![](https://github.com/vizzTools/dem3d/blob/master/docs/dem3d_example.gif)
