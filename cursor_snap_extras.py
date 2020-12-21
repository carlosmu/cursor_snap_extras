# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


bl_info = {
    "name" : "Cursor Snap Extras",
    "author" : "carlosmu <carlos.damian.munoz@gmail.com>",    
    "blender" : (2, 83, 0),
    "version" : (0, 1, 0),
    "category" : "Animation",
    "location" : "Pose Context Menu",
    "description" : "Snap Location and Rotation from/to 3d Cursor.",
    "warning" : "",
    "doc_url" : "https://github.com/carlosmu/cursor_snap_extras",
    "tracker_url" : "",
}

import bpy

#########################################
# Operator: Active Bone to Cursor       #
#########################################
class CSE_OT_active_bone_to_cursor(bpy.types.Operator):
    """Active Bone Location/Rotation to cursor"""
    bl_idname = "cse.active_bone_to_cursor"
    bl_label = "Active Bone to Cursor"

    # Only appears on 3D VIEW
    @classmethod
    def poll(cls, context):
        return context.area.ui_type == 'VIEW_3D'
    
    def execute(self, context):        
        # Variables
        cursor = bpy.context.scene.cursor
        bone_active = bpy.context.active_pose_bone
        # Move active bone to cursor position
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
        # Rotate active bone to cursor rotation (Quaternion or Euler)
        if bone_active.rotation_mode == 'QUATERNION':
            bone_active.rotation_quaternion = cursor.rotation_euler.to_quaternion()
        else:
            bone_active.rotation_euler = cursor.rotation_euler
        return{'FINISHED'}

#########################################
# Operator: Cursor to Active Bone       #
#########################################
class CSE_OT_cursor_to_active_bone(bpy.types.Operator):
    """Cursor Location/Rotation to active bone"""
    bl_idname = "cse.cursor_to_active_bone"
    bl_label = "Cursor to Active Bone"

    # Only appears on 3D VIEW
    @classmethod
    def poll(cls, context):
        return context.area.ui_type == 'VIEW_3D'
    
    def execute(self, context):
        # Variables
        cursor = bpy.context.scene.cursor
        bone_active = bpy.context.active_pose_bone
        # Cursor to Active Bone Position
        bpy.ops.view3d.snap_cursor_to_selected()   
        # Cursor to Active Bone Rotation (Quaternion or Euler)
        if bone_active.rotation_mode == 'QUATERNION':
            cursor.rotation_euler = bone_active.rotation_quaternion.to_euler()
        else:            
            cursor.rotation_euler = bone_active.rotation_euler
        return{'FINISHED'}

###############################
# Draw buttons on contextMenu #
###############################
def draw_extra_pose_menues(self, context):
    layout = self.layout
    # Menu elements on selected pose bones
    if context.selected_pose_bones:
        layout.operator("cse.active_bone_to_cursor",icon='RESTRICT_SELECT_OFF') # Set Selected Loc/Rot to
        layout.operator("cse.cursor_to_active_bone",icon='CURSOR') # Set Cursor Loc/Rot to selected
        # Separator
        layout.separator()

##########################
# Register/Unregister    #
##########################
def register():
    bpy.utils.register_class(CSE_OT_active_bone_to_cursor)
    bpy.utils.register_class(CSE_OT_cursor_to_active_bone)    
    bpy.types.VIEW3D_MT_pose_context_menu.prepend(draw_extra_pose_menues) 
        
def unregister():
    bpy.utils.unregister_class(CSE_OT_active_bone_to_cursor)
    bpy.utils.unregister_class(CSE_OT_cursor_to_active_bone)
    bpy.types.VIEW3D_MT_pose_context_menu.remove(draw_extra_pose_menues)