import bpy
from bpy.props          import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types          import (Menu, Panel, Operator, AddonPreferences, PropertyGroup)


# -----------------------------------------------------------------------------
#   Modifier Visibility Pie
# ----------------------------------------------------------------------------- 

class VIEW3D_MT_ntzbu_modifier_tools_pie(Menu):
    bl_label = "NTZBU : Modifier Tools"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        pie = layout.menu_pie()

        #LEFT
        op = pie.operator("view3d.ntzbu_apply_modifiers", text="Apply", icon="CHECKMARK")


        #RIGHT
        op = pie.operator("view3d.ntzbu_remove_modifiers", text="Remove", icon="PANEL_CLOSE")

        #BOTTOM
        popoverBtn = pie.popover(text="Configure", panel="VIEW3D_PT_ntzbu_modifier_tools_options", icon="SETTINGS")
        
        
        #TOP
        op = pie.operator("view3d.ntzbu_modifier_visibility", text="Toggle")
        op.enableDisableToggle = "TOGGLE"
        op.tooltip = "Toggle Modifiers.  Default: Selected Objects.  SHIFT: All Objects.  CTRL: Unselected objects"
        
        #TOP LEFT
        op = pie.operator("view3d.ntzbu_modifier_visibility", text="Enable", icon="HIDE_OFF")
        op.enableDisableToggle = "ENABLE"
        op.tooltip = "Enable Modifiers.  Default: Selected Objects.  SHIFT: All Objects.  CTRL: Unselected objects"

        
        #TOP RIGHT

        op = pie.operator("view3d.ntzbu_modifier_visibility", text="Disable", icon="HIDE_ON")
        op.enableDisableToggle = "DISABLE"
        op.tooltip = "Disable Modifiers.  Default: Selected Objects.  SHIFT: All Objects.  CTRL: Unselected objects"

        
        #BOTTOM LEFT
        op = pie.operator("view3d.ntzbu_open_modifiers_sidebar", text="Modifiers", icon="HIDE_OFF")

        
        #BOTTOM RIGHT
        pie.menu(menu="MESH_MT_ml_add_modifier_menu", text="Add Modifier", text_ctxt="", translate=True, icon='MODIFIER_ON', icon_value=0)




# -----------------------------------------------------------------------------
#   Operator which calls the modifier list pie
# ----------------------------------------------------------------------------- 

class VIEW3D_OT_ntzbu_modifier_tools_pie(Operator):

    """Tooltip"""
    bl_idname           = "view3d.ntzbu_modifier_tools_pie"
    bl_label            = "NTZBU : Modifier Tools Pie"
    bl_description      = "Modifier Tools - Pie"
    bl_options          = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_ntzbu_modifier_tools_pie")
        
        return {'FINISHED'}
    # END execute()

# END Operator()