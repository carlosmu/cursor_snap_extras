import bpy
import mathutils
import math

"""
TO-DO:
Lo que está faltando es incluir a los constrains. De alguna manera debería poder aplicar el visual transform del bone al cursor, y después volver a aplicarlo al otro bone. 
Por ejemplo al rotar el root en rigify deja de funcionar, porque el root no es parent del ik_foot, sino que está asociado por un constraint.
Revisar la función bpy.ops.pose.visual_transform_apply()
"""

### FUNCTIONS ###

# Devuelve la rotacion del hueso en quaternion (no soporta axis angle)
def get_bone_rotation(bone):
    bone_rotation = mathutils.Quaternion()

    if bone.rotation_mode != 'QUATERNION':
        bone_rotation = bone.rotation_euler.to_quaternion()
    else:
        bone_rotation = bone.rotation_quaternion
        
    return bone_rotation


# Devuelve la rotación que permite convertir coordenadas locales a globales
def get_parent_world_rotation(bone):    
    parent = bone.parent
    rotation = mathutils.Quaternion()    

    while parent != None:            
        rotation = rotation @ get_bone_rotation(parent)
#        print(get_bone_rotation(parent).to_euler())  
        parent = parent.parent               

    return rotation   


# Devuelve una rotación que permite convertir coordenadas globales a locales
def get_parent_local_rotation(bone):
    return get_parent_world_rotation(bone).inverted()


# Devuelve la rotacion global de un hueso, teniendo en cuenta toda su jerarquía
def get_bone_world_rotation(bone):
    return get_parent_world_rotation(bone) @ get_bone_rotation(bone)
    


### VARIABLES ###
bone = bpy.context.active_pose_bone
cursor = bpy.context.scene.cursor
armature = bpy.context.active_object


# Asigna la rotación al cursor
#cursor.rotation_euler = get_bone_world_rotation(bone).to_euler()

# Asigna la rotación al bone activo
bone.rotation_quaternion = get_bone_rotation(armature).inverted() @ get_parent_local_rotation(bone) @ cursor.rotation_euler.to_quaternion()
print(armature.rotation_euler)

