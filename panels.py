import bpy
from .utils import calculate_bone_angle, check_vrm_blendshapes, check_eye_bones

class OT_CalcTrisCount(bpy.types.Operator):
    bl_idname = "object.calc_tris_count"
    bl_label = "Calculate Triangles"
    mesh_name: bpy.props.StringProperty()

    def execute(self, context):
        obj = bpy.data.objects.get(self.mesh_name)
        if obj and obj.type == 'MESH':
            mesh = obj.data
            mesh.calc_loop_triangles()
            tris_count = len(mesh.loop_triangles)
            self.report({'INFO'}, f"Triangles in '{obj.name}': {tris_count}")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "Object not found or not a mesh")
            return {'CANCELLED'}


class VIEW3D_PT_TriCountPanel(bpy.types.Panel):
    bl_label = "Triangle Count"
    bl_idname = "VIEW3D_PT_tricount_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Avatar_Analyzer"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj and obj.type == 'MESH':
            mesh = obj.data
            mesh.calc_loop_triangles()
            tris_count = len(mesh.loop_triangles)
            layout.label(text=f"Selected Mesh: {obj.name}")
            layout.label(text=f"Triangles: {tris_count}")
            layout.operator("object.calc_tris_count", text="Recalculate").mesh_name = obj.name
        else:
            layout.label(text="Select a mesh object.")


class VIEW3D_PT_MaterialSlotsPanel(bpy.types.Panel):
    bl_label = "Material Slots"
    bl_idname = "VIEW3D_PT_material_slots_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Avatar_Analyzer"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj and obj.type == 'MESH':
            layout.label(text=f"Selected Mesh: {obj.name}")
            layout.label(text=f"Material Slots: {len(obj.material_slots)}")
        else:
            layout.label(text="Select a mesh object.")


class VIEW3D_PT_VRM_BlendShapesPanel(bpy.types.Panel):
    bl_label = "Check VRM Blendshapes"
    bl_idname = "VIEW3D_PT_VRM_blendshapes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Avatar_Analyzer"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if not obj:
            layout.label(text="No object selected")
            return

        missing, _ = check_vrm_blendshapes(obj)

        if missing:
            layout.label(text="Missing Blendshapes:")
            for bs in missing:
                layout.label(text=f" - {bs}")


class VIEW3D_PT_bone_angle_panel(bpy.types.Panel):
    bl_label = "Bone Angle Tool"
    bl_idname = "VIEW3D_PT_bone_angle_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Avatar_Analyzer"

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
            
class VIEW3D_PT_CheckEyeBonesPanel(bpy.types.Panel):
    bl_label = "Check Eye Bones"
    bl_idname = "VIEW3D_PT_check_eye_bones"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Avatar_Analyzer"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if not obj or obj.type != 'ARMATURE':
            layout.label(text="Please select an armature.")
            return

        left_eye_name = "EyeBone.L"
        right_eye_name = "EyeBone.R"
        found_left, found_right = check_eye_bones(obj.data, left_eye_name, right_eye_name)

        layout.label(text=f"Expected: {left_eye_name}, {right_eye_name}")

        if found_left and found_right:
            layout.label(text="✅ Eye bones found. Good to go!")
        else:
            if not found_left:
                layout.label(text=f"❌ Missing: {left_eye_name}")
            if not found_right:
                layout.label(text=f"❌ Missing: {right_eye_name}")
            layout.label(text="Please add the missing eye bones.")



classes = [
    OT_CalcTrisCount,
    VIEW3D_PT_TriCountPanel,
    VIEW3D_PT_MaterialSlotsPanel,
    VIEW3D_PT_VRM_BlendShapesPanel,
    VIEW3D_PT_bone_angle_panel,
    VIEW3D_PT_CheckEyeBonesPanel
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
