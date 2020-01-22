import bpy
from . props_misc import NTZBNSUTLS_selcontigedgprops
from . import misc_functions
from . import lay_misc

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#   Panel
# ----------------------------------------------------------------------------- 


class NTZBNSUTLS_PT_selcontigedgoptions(Panel):
    bl_label = "Neltulz - Bonus Utils - Sel Contig Edges Options"
    bl_idname = "NTZBNSUTLS_PT_selcontigedgoptions"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        layout.ui_units_x = 15

        optionsSection = layout.column(align=True)

        lay_misc.selContigEdgesSettings(self, context, scn, optionsSection)
    
    #END draw()
#END Panel

class NTZBNSUTLS_PT_modifiertoolsoptions(Panel):
    bl_label = "Neltulz - Bonus Utils - Modifier Tools Options"
    bl_idname = "NTZBNSUTLS_PT_modifiertoolsoptions"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        layout.ui_units_x = 15

        optionsSection = layout.column(align=True)

        lay_misc.modifierToolsOptions(self, context, scn, optionsSection)
    
    #END draw()
#END Panel


class NTZBNSUTLS_PT_sidebarpanel(Panel):
    bl_label = "Bonus Utils v1.0.1"
    bl_category = "Neltulz"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    bUseCompactSidebarPanel = BoolProperty(
        name="Use Compact Panel",
        description="Use Compact Panel",
        default = False
    )

    bUseCompactPopupAndPiePanel = BoolProperty(
        name="Use Compact Popup & Pie Panel",
        description="Use Compact Popup & Pie Panel",
        default = True
    )

    def draw(self, context):
        lay_misc.mainBonusUtilsPanel(self, context, self.bUseCompactSidebarPanel, self.bUseCompactPopupAndPiePanel)