bl_info = {
    "name": "AvatarAnalyzer",
    "author": "hemaraju_gowda",
    "version": (1, 0),
    "blender": (4, 3, 0),
    "location": "View3D > Sidebar > MyAddon Tab",
    "description": "Displays the angle between two selected bones",
    "category": "mesh",
}


import bpy
from . import VIEW3D_PT_bone_angle_panel
from bpy.props import PointerProperty, StringProperty


class BoneAngleProperties(bpy.types.PropertyGroup):
    bone_a: StringProperty(name="Bone A")
    bone_b: StringProperty(name="Bone B")


classes = [
    BoneAngleProperties,
    VIEW3D_PT_bone_angle_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.bone_angle_props = PointerProperty(type=BoneAngleProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.bone_angle_props

if __name__ == "__main__":
    register()