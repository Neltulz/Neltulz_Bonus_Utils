#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Name        : All-in-one Tool Settings Popup
# Description : Popup containing a lot of tool settings
# Author      : Neltulz (Neil V. Moore)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import bpy
import time
from bpy.types                 import VIEW3D_PT_active_tool, VIEW3D_PT_tools_meshedit_options, VIEW3D_PT_tools_meshedit_options_automerge, VIEW3D_PT_tools_object_options_transform, VIEW3D_PT_transform_orientations, VIEW3D_PT_snapping, VIEW3D_PT_proportional_edit

from bpy.props                 import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types                 import (Panel, Operator, AddonPreferences, PropertyGroup)

from .                         import misc_functions
from .                         import lay_misc


class LayoutEngine:
    def __init__(self, layout):
        self.layout = layout

class NTZBNSUTLS_OT_aiotoolsettings(Operator):

    """Tooltip"""
    bl_idname = "ntzbnsutls.aiotoolsettings"
    bl_label = "Neltulz - Bonus Utils : All-in-One Tool Settings"
    bl_description = "Popup containing a lot of tool settings"
    bl_options = {'REGISTER'}

    usePopupWithOK : BoolProperty (
        name="Use Popup With OK Button",
        description='Adds an "OK" button to the popup and prevents the popup from disappearing until you explicitly click OK or click outside of the popup.',
        default = False,
    )
    

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):

        activeObjAtBegin = bpy.context.view_layer.objects.active

        lay = self.layout
        lay = lay.column(align=True)
        scn = context.scene


        if not self.usePopupWithOK:
            lay.label(text="Neltulz - Bonus Utils : All-in-One Tool Settings")
            lay.separator()

        row = lay.row(align=True)

        verticalSpacer = row.row(align=True)

        verticalSpacer.scale_y = 17.2
        verticalSpacer.scale_x = 0.1
        verticalSpacer.label(text=" ")
        
        grid = row.grid_flow(align=False, even_columns=True, columns=5)


        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # Move Tool Section
        #-----------------------------------------------------------------------------------------------------------------------------------------------

        box = grid.box().column(align=False)

        layEngine = LayoutEngine(box)
        layEngine.bl_space_type = 'VIEW_3D'
        
        VIEW3D_PT_active_tool.draw(layEngine, context)

        box.separator()


        if activeObjAtBegin is not None:
            if activeObjAtBegin.type == "MESH":

                layEngine = LayoutEngine(box)
                layEngine.bl_space_type = 'VIEW_3D'

                VIEW3D_PT_tools_meshedit_options.draw(layEngine, context)

        

        mergeBox = box.box()

        mergeBox.prop(context.tool_settings, "use_mesh_automerge", text="Auto Merge", text_ctxt="", translate=True, icon='NONE', expand=False, slider=False, toggle=0, icon_only=False, event=False, full_event=False, emboss=True, index=0, icon_value=0, invert_checkbox=False)

        layEngine = LayoutEngine(mergeBox)
        layEngine.bl_space_type = 'VIEW_3D'

        VIEW3D_PT_tools_meshedit_options_automerge.draw(layEngine, context)

        box.separator()
        transformAffectBox = box.box()

        layEngine = LayoutEngine(transformAffectBox)
        layEngine.bl_space_type = 'VIEW_3D'

        VIEW3D_PT_tools_object_options_transform.draw(layEngine, context)


        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # Transform Orientation Section
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        
        box = grid.box().column(align=False)

        VIEW3D_PT_transform_orientations.draw(LayoutEngine(box), context)

        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # Pivot Section
        #-----------------------------------------------------------------------------------------------------------------------------------------------

        box = grid.box().column(align=False)

        box.label(text="Pivot")
        box.prop(scn.tool_settings, "transform_pivot_point", expand=True)
       
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # Snap Section
        #-----------------------------------------------------------------------------------------------------------------------------------------------

        box = grid.box().column(align=False)

        box.prop(context.tool_settings, "use_snap", text="Snap", toggle=1, expand=True)

        box.separator()

        col = box.column(align=True)
        if not context.tool_settings.use_snap:
            col.active = False
        VIEW3D_PT_snapping.draw(LayoutEngine(col), context)

        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # Proportional Falloff Section
        #-----------------------------------------------------------------------------------------------------------------------------------------------

        box = grid.box().column(align=False)

        box.prop(context.tool_settings, "use_proportional_edit", text="Proportional Edit", toggle=1, expand=True)

        box.separator()

        col = box.column(align=True)
        if not context.tool_settings.use_proportional_edit:
            col.active = False

        col.label(text="Proportional Falloff")
        VIEW3D_PT_proportional_edit.draw(LayoutEngine(col), context)
            

    # END draw()


    def execute(self, context):
        return {'FINISHED'}
    # END execute()


    def invoke(self, context, event):
        region = context.region
        rx = region.x
        ry = region.y
        rw = region.width
        rh = region.height


        popHeightFull = 350
        
        if self.usePopupWithOK:
            popWidthHalf = 0
            mouseVOffsetPre = 145
            mouseVOffsetPost = 120
        else:
            popWidthHalf = 500
            mouseVOffsetPre = 130
            mouseVOffsetPost = 120

        mxy = (rx + event.mouse_region_x, ry + event.mouse_region_y + mouseVOffsetPost)
        
        
        context.window.cursor_warp(rx + event.mouse_region_x - popWidthHalf, ry + event.mouse_region_y + popHeightFull + mouseVOffsetPre)

        # spawn popup
        if self.usePopupWithOK:
            popup = context.window_manager.invoke_props_dialog(self, width=1000)
        else:
            popup = context.window_manager.invoke_popup(self, width=1000)

        #move cursor back to original location
        context.window.cursor_warp(*mxy)

        return popup

    # END invoke()

# END Operator()