def calculate_bone_angle(context, bone_name_a, bone_name_b):
    obj = context.object

    if not obj or obj.type != 'ARMATURE' or context.mode != 'POSE':
        return None

    pose_bones = obj.pose.bones

    if bone_name_a not in pose_bones or bone_name_b not in pose_bones:
        return None

    bone_a = pose_bones[bone_name_a]
    bone_b = pose_bones[bone_name_b]

    # Bone direction vectors in world space
    vec_a = (obj.matrix_world @ bone_a.tail) - (obj.matrix_world @ bone_a.head)
    vec_b = (obj.matrix_world @ bone_b.tail) - (obj.matrix_world @ bone_b.head)

    # Normalize
    vec_a.normalize()
    vec_b.normalize()

    # Angle between vectors
    angle_rad = vec_a.angle(vec_b)
    angle_deg = math.degrees(angle_rad)

    return angle_deg