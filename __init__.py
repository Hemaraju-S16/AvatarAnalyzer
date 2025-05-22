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
from . import panels, utils
from . import properties

def register():
    bpy.utils.register_class(properties.BoneAngleProperties)
    bpy.types.Scene.bone_angle_props = bpy.props.PointerProperty(type=properties.BoneAngleProperties)
    utils.register()
    panels.register()
    
    

def unregister():
    for cls in reversed(panels.classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.bone_angle_props
    bpy.utils.unregister_class(properties.BoneAngleProperties)
    panels.unregister()
    utils.unregister()
    

    



if __name__ == "__main__":
    register()