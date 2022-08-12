"""Set up a Blender Scene with a DEM as a mesh a list of rasters as an animated texture.

Uses BlenderGIS to ease the creation amb surface + texture.
"""
from dataclasses import dataclass
import math
from pathlib import Path

import bpy  # noqa: E0401
from mathutils import Euler  # noqa: E0401


@dataclass
class Camera:
    """Camera class to control blender camera parameters."""

    location: tuple[float, float, float]
    rotation: tuple[float, float, float]
    clip_end: float = 100_000
    type: str = "PERSP"
    lens_unit: str = "FOV"
    angle: float = 45

    def euler_rotation_in_radians(self):
        """Get the rotation in radians."""
        return Euler(math.radians(v) for v in self.rotation)

    def angle_in_radians(self):
        """Get the angle in radians."""
        return math.radians(self.angle)

    def set_camera_obj(self, camera_obj):
        """Modify the blender camera object with the instance parameters."""
        camera_obj.location = self.location
        camera_obj.rotation_euler = self.euler_rotation_in_radians()
        camera_obj.data.clip_end = self.clip_end
        camera_obj.data.type = self.type
        camera_obj.data.lens_unit = self.lens_unit
        camera_obj.data.angle = self.angle_in_radians()


@dataclass
class Light:
    """Light class to control blender light parameters."""

    location: tuple[float, float, float]
    rotation: tuple[float, float, float]
    type: str = "SUN"
    energy: float = 15

    def euler_rotation_in_radians(self):
        """Get the rotation in radians."""
        return Euler(math.radians(v) for v in self.rotation)

    def set_light_obj(self, light_obj):
        """Modify the blender light object with the instance parameters."""
        light_obj.data.energy = self.energy
        light_obj.data.type = self.type
        light_obj.location = self.location
        light_obj.rotation_euler = self.euler_rotation_in_radians()


def make_dem_with_texture(dem_path: Path, rasters: list[Path], strength: float = 1):
    """Create a blender scene with a mesh and texture from a dem file and a list of rasters."""
    # Remove already existing meshes
    # Select objects by type
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            obj.select_set(True)
        else:
            obj.select_set(False)
    bpy.ops.object.delete()

    bpy.ops.importgis.georaster(
        filepath=str(dem_path),
        importMode="DEM",
    )
    bpy.ops.importgis.georaster(filepath=str(rasters[0]), importMode="MESH")
    nodes = bpy.data.materials["rastMat"].node_tree.nodes

    # use the created material ("rastMat") node and convert it into a image sequence
    img_texture_node = nodes["Image Texture"]
    img_texture_node.image.source = "SEQUENCE"

    img_texture_node.image.filepath = str(rasters[0])

    # change the material properties
    nodes["Principled BSDF"].inputs["Roughness"].default_value = 1
    nodes["Principled BSDF"].inputs["Specular"].default_value = 0

    # parameters for how the image data is used by anoter data-block are under ImageUser
    img_texture_node.image_user.frame_duration = len(rasters)
    # TODO: set offset from file name pattern
    img_texture_node.image_user.frame_offset = 1984
    img_texture_node.image_user.use_auto_refresh = True
    img_texture_node.image_user.use_cyclic = True
    img_texture_node.update()

    bpy.data.objects["elevation.3857"].modifiers["DEM.001"].strength = strength

    # Camera
    camera = Camera(location=(32583.0, -27174.0, 14000.0), rotation=(71.0, 0.0, 50.0), angle=30)
    camera.set_camera_obj(bpy.data.objects["Camera"])

    # Lights
    light = Light(
        location=(4.0, 1.0, 11000.0),
        rotation=(70.0, -38.0, 25.0),
    )
    light_obj = bpy.data.objects["Light"]
    light.set_light_obj(light_obj)
