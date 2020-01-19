import bpy
from bpy.props          import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types          import (Menu, Panel, Operator, AddonPreferences, PropertyGroup)

from . props_misc       import NTZBNSUTLS_mdfrtoolsprops


# -----------------------------------------------------------------------------
#   Modifier Visibility Pie
# ----------------------------------------------------------------------------- 

class NTZBNSUTLS_MT_modifiertoolspie(Menu):
    bl_label = "Modifier Tools"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        pie = layout.menu_pie()

        #LEFT
        op = pie.operator("ntzbnsutls.applymodifiers", text="Apply", icon="CHECKMARK")
        if scn.ntzbnsutls_mdfrtools.useCustomModifierVisibilitySettings == "CUSTOM": op.bForcePanelOptions = True


        #RIGHT
        op = pie.operator("ntzbnsutls.removemodifiers", text="Remove", icon="PANEL_CLOSE")

        #BOTTOM
        popoverBtn = pie.popover(text="Configure", panel="NTZBNSUTLS_PT_modifiertoolsoptions", icon="SETTINGS")
        
        
        #TOP
        op = pie.operator("ntzbnsutls.modifiervisibility", text="Toggle")
        op.enableDisableToggle = "TOGGLE"
        if scn.ntzbnsutls_mdfrtools.useCustomModifierVisibilitySettings == "CUSTOM": op.bForcePanelOptions = True
        op.tooltip = "Toggle Modifiers.  Default: Selected Objects.  SHIFT: All Objects.  CTRL: Unselected objects"
        
        #TOP LEFT
        op = pie.operator("ntzbnsutls.modifiervisibility", text="Enable", icon="HIDE_OFF")
        op.enableDisableToggle = "ENABLE"
        if scn.ntzbnsutls_mdfrtools.useCustomModifierVisibilitySettings == "CUSTOM": op.bForcePanelOptions = True
        op.tooltip = "Enable Modifiers.  Default: Selected Objects.  SHIFT: All Objects.  CTRL: Unselected objects"

        
        #TOP RIGHT

        op = pie.operator("ntzbnsutls.modifiervisibility", text="Disable", icon="HIDE_ON")
        op.enableDisableToggle = "DISABLE"
        if scn.ntzbnsutls_mdfrtools.useCustomModifierVisibilitySettings == "CUSTOM": op.bForcePanelOptions = True
        op.tooltip = "Disable Modifiers.  Default: Selected Objects.  SHIFT: All Objects.  CTRL: Unselected objects"

        
        #BOTTOM LEFT
        op = pie.operator("ntzbnsutls.openmodifiersidebar", text="Modifiers", icon="HIDE_OFF")

        
        #BOTTOM RIGHT
        pie.menu(menu="MESH_MT_ml_add_modifier_menu", text="Add Modifier", text_ctxt="", translate=True, icon='MODIFIER_ON', icon_value=0)




# -----------------------------------------------------------------------------
#   Operator which calls the modifier list pie
# ----------------------------------------------------------------------------- 

class NTZBNSUTLS_OT_modifiertoolspie(Operator):

    """Tooltip"""
    bl_idname = "ntzbnsutls.modifiertoolspie"
    bl_label = "Neltulz - Bonus Utils : Modifier Tools Pie"
    bl_description = "Modifier Tools - Pie"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="NTZBNSUTLS_MT_modifiertoolspie")
        
        return {'FINISHED'}
    # END execute()

# END Operator()