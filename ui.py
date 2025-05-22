import bpy
from operators import calculate_bone_angle

class VIEW3D_PT_bone_angle_panel(bpy.types.Panel):
    bl_label = "Bone Angle Tool"
    bl_idname = "VIEW3D_PT_bone_angle_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MyAddon"

    def draw(self, context):
        layout = self.layout
        props = context.scene.bone_angle_props

        layout.prop(props, "bone_a")
        layout.prop(props, "bone_b")

        angle = calculate_bone_angle(context, props.bone_a, props.bone_b)
        if angle is not None:
            layout.label(text=f"Angle: {angle:.2f}°")
        else:
            layout.label(text="Select valid bones")