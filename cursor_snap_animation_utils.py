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
    "name" : "Cursor Snap Animation Utils",
    "author" : "carlosmu <carlos.damian.munoz@gmail.com>",    
    "blender" : (2, 91, 0),
    "version" : (0, 0, 1),
    "category" : "Animation",
    "location" : "Pose Context Menu",
    "description" : "Snap Location and Rotation to/from 3d Cursor. Only Support Eulers",
    "warning" : "",
    "doc_url" : "",
    "tracker_url" : "",
}

import bpy

#########################################
# Operator: Selected Bone to Cursor     #
#########################################
class CSAU_OT_selected_to_cursor(bpy.types.Operator):
    """Location/Rotation from bones to cursor (only support euler)"""
    bl_idname = "csau.selected_to_cursor"
    bl_label = "Bone Loc/Rot to Cursor"

    # Only appears on 3D VIEW
    @classmethod
    def poll(cls, context):
        return context.area.ui_type == 'VIEW_3D'
    
    def execute(self, context):
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
        bpy.context.active_pose_bone.rotation_euler = bpy.context.scene.cursor.rotation_euler
        return{'FINISHED'}


#########################################
# Operator: Cursor to Selected Bone     #
#########################################
class CSAU_OT_cursor_to_selected(bpy.types.Operator):
    """Location/Rotation from cursor to bones (only support euler)"""
    bl_idname = "csau.cursor_to_selected"
    bl_label = "Cursor Loc/Rot to Bone"

    # Only appears on 3D VIEW
    @classmethod
    def poll(cls, context):
        return context.area.ui_type == 'VIEW_3D'
    
    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.context.scene.cursor.rotation_euler = bpy.context.active_pose_bone.rotation_euler
        return{'FINISHED'}

###############################
# Draw buttons on contextMenu #
###############################
def draw_extra_menues(self, context):
    layout = self.layout
    # Menu elements on selected pose bones
    if context.selected_pose_bones:
        layout.operator("csau.selected_to_cursor",icon='RESTRICT_SELECT_OFF') # Set Selected Loc/Rot to
        layout.operator("csau.cursor_to_selected",icon='CURSOR') # Set Cursor Loc/Rot to selected
        # Separator
        layout.separator()


##########################
# Register/Unregister    #
##########################
def register():
    bpy.utils.register_class(CSAU_OT_selected_to_cursor)
    bpy.utils.register_class(CSAU_OT_cursor_to_selected)    
    bpy.types.VIEW3D_MT_pose_context_menu.prepend(draw_extra_menues) 
        
def unregister():
    bpy.utils.unregister_class(CSAU_OT_selected_to_cursor)
    bpy.utils.unregister_class(CSAU_OT_cursor_to_selected)
    bpy.types.VIEW3D_MT_pose_context_menu.remove(draw_extra_menues)
