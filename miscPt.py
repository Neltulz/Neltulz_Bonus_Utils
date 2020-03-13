import bpy
from . import miscFunc
from . import miscLay

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#   Panel
# ----------------------------------------------------------------------------- 


class VIEW3D_PT_ntzbu_delete_all_unselected_objects_options(Panel):
    bl_label            = 'NTZBU : "Delete Unselected Objects" Options'
    bl_idname           = 'VIEW3D_PT_ntzbu_delete_all_unselected_objects_options'
    bl_category         = ''
    bl_space_type       = 'VIEW_3D'
    bl_region_type      = 'WINDOW'

    def draw(self, context):
        scn = context.scene
        lay = self.layout
        lay.ui_units_x = 20

        addonPrefs = context.preferences.addons[__package__].preferences

        header = lay.row(align=True)
        header.label(text='"Group with Empty" Options:', icon="EMPTY_DATA")
        header.separator()

        box = lay.box().column(align=True)

        miscLay.delUnselObjs_options(addonPrefs, context, lay=box)
    
    #END draw()
#END Panel

class VIEW3D_PT_ntzbu_group_with_empty_options(Panel):
    bl_label            = 'NTZBU : "Group With Empty" Options'
    bl_idname           = 'VIEW3D_PT_ntzbu_group_with_empty_options'
    bl_category         = ''
    bl_space_type       = 'VIEW_3D'
    bl_region_type      = 'WINDOW'

    def draw(self, context):
        scn = context.scene
        lay = self.layout
        lay.ui_units_x = 20

        addonPrefs = context.preferences.addons[__package__].preferences

        header = lay.row(align=True)
        header.label(text='"Group with Empty" Options:', icon="EMPTY_DATA")
        header.separator()

        box = lay.box().column(align=True)

        miscLay.groupWithEmpty_options(addonPrefs, context, lay=box)
    
    #END draw()
#END Panel

class VIEW3D_PT_ntzbu_select_contiguous_edges_options(Panel):
    bl_label            = 'NTZBU : "Sel Contig Edges" Options'
    bl_idname           = 'VIEW3D_PT_ntzbu_select_contiguous_edges_options'
    bl_category         = ''
    bl_space_type       = 'VIEW_3D'
    bl_region_type      = 'WINDOW'

    def draw(self, context):
        scn = context.scene
        lay = self.layout
        lay.ui_units_x = 20

        addonPrefs = context.preferences.addons[__package__].preferences

        header = lay.row(align=True)
        header.label(text='"Select Contiguous Edges" Options:', icon="SNAP_MIDPOINT")
        header.separator()

        box = lay.box().column(align=True)

        miscLay.selContigEdg_options(addonPrefs, context, lay=box)
    
    #END draw()
#END Panel



class VIEW3D_PT_ntzbu_modifier_tools_options(Panel):
    bl_label            = 'NTZBU : "Modifier Tools" Options'
    bl_idname           = 'VIEW3D_PT_ntzbu_modifier_tools_options'
    bl_category         = ''
    bl_space_type       = 'VIEW_3D'
    bl_region_type      = 'WINDOW'

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        layout.ui_units_x = 15

        optionsSection = layout.column(align=True)

        miscLay.modifierToolsOptions(self, context, scn, optionsSection)
    
    #END draw()
#END Panel


class VIEW3D_PT_ntzbu_sidebar_panel(Panel):
    bl_label            = 'Bonus Utils v1.0.4'
    bl_category         = 'Neltulz'
    bl_space_type       = 'VIEW_3D'
    bl_region_type      = 'UI'

    bUseCompactSidebarPanel = BoolProperty(
        name            = 'Use Compact Panel',
        description     = 'Use Compact Panel',
        default         = False
    )

    bUseCompactPopupAndPiePanel = BoolProperty(
        name            = 'Use Compact Popup & Pie Panel',
        description     = 'Use Compact Popup & Pie Panel',
        default         = True
    )

    def draw(self, context):
        miscLay.mainBonusUtilsPanel(self, context, self.bUseCompactSidebarPanel, self.bUseCompactPopupAndPiePanel)