import math
import bpy
from mathutils import Vector

def calculate_bone_angle(context, bone_name_a, bone_name_b):
    obj = context.object

    if not obj or obj.type != 'ARMATURE' or context.mode != 'POSE':
        return None

    pose_bones = obj.pose.bones

    if bone_name_a not in pose_bones or bone_name_b not in pose_bones:
        return None

    bone_a = pose_bones[bone_name_a]
    bone_b = pose_bones[bone_name_b]

    vec_a = (obj.matrix_world @ bone_a.tail) - (obj.matrix_world @ bone_a.head)
    vec_b = (obj.matrix_world @ bone_b.tail) - (obj.matrix_world @ bone_b.head)

    vec_a.normalize()
    vec_b.normalize()

    angle_rad = vec_a.angle(vec_b)
    return math.degrees(angle_rad)


def check_vrm_blendshapes(mesh_obj):
    vrm_blendshapes = [
        "A", "I", "U", "E", "O",
        "Blink", "Blink_L", "Blink_R",
        "Joy", "Angry", "Sorrow", "Fun", "Neutral",
        "LookUp", "LookDown", "LookLeft", "LookRight"
    ]

    if not mesh_obj or mesh_obj.type != 'MESH':
        print("Provided object is not a mesh")
        return [], None

    if not mesh_obj.data.shape_keys:
        print(f"Mesh '{mesh_obj.name}' has no shape keys.")
        return [], None

    shape_keys = mesh_obj.data.shape_keys.key_blocks
    missing_bs = [bs_name for bs_name in vrm_blendshapes if bs_name not in shape_keys]

    return missing_bs, None


def check_eye_bones(armature_data, left_eye_name="EyeBone.L", right_eye_name="EyeBone.R"):
    bone_names = [bone.name for bone in armature_data.bones]
    found_left = any(left_eye_name in name for name in bone_names)
    found_right = any(right_eye_name in name for name in bone_names)
    return found_left, found_right



def register():
    pass


def unregister():
    pass
