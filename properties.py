import bpy

class BoneAngleProperties(bpy.types.PropertyGroup):
    bone_a: bpy.props.StringProperty(name="Bone A")
    bone_b: bpy.props.StringProperty(name="Bone B")
