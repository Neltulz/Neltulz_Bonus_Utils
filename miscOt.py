import bpy
from . import miscFunc

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#   Reset Settings
# -----------------------------------------------------------------------------    

class VIEW3D_OT_ntzbu_reset_settings(Operator):
    """Tooltip"""
    bl_idname           = "view3d.ntzbu_reset_settings"
    bl_label            = "NTZBU : Reset Setting(s)"
    bl_description      = "Resets setting(s)"

    settingsPropList_List = (
        ('SELCONTIGEDG',  "Select Contiguous Edges - Reset Prop List",  "", "", 0),
        ('MDFRTOOLS',       "Modifier Visibility - Reset Prop List",      "", "", 1),
    )

    settingsPropList : EnumProperty(
        items			= settingsPropList_List,
        name			= "Settings Prop List",
        description		= "Settings Prop List to Use",
    )


    #Select Contiguous Edge - Reset List
    selcontigedg_settingsToReset_List = [
        ("maxAngle",  "Max Angle", "", "", 1 << 2),
        ("maxEdges",  "Max Edges", "", "", 1 << 3),
        ("direction", "Direction", "", "", 1 << 4),
    ]

    selcontigedg_settingsToReset : EnumProperty (
        options={'ENUM_FLAG'},
        items=selcontigedg_settingsToReset_List,
        name="Select Contiguous Setting(s) to Reset",
        description='Name of the setting(s) to be reset',
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scn = context.scene

        if self.settingsPropList == "SELCONTIGEDG":
            data = scn.ntzbnsutls_selcontigedg
            propNameList = self.selcontigedg_settingsToReset

        for propName in propNameList:
            
            defaultVal = data.__annotations__[propName][1]['default']
            setattr(data, propName, defaultVal)

        propNameList.clear()

        return {'FINISHED'}
    # END execute()
# END Operator()


# -----------------------------------------------------------------------------
#   Toggle Section
# -----------------------------------------------------------------------------    

class WM_OT_ntzbu_toggle_section(Operator):
    """Tooltip"""
    bl_idname           = "wm.ntzbu_toggle_section"
    bl_label            = "NTZBU : Toggle Section"
    bl_description      = "Toggle Section"

    data : StringProperty (
        default = '',
    )

    group : StringProperty (
        default = '',
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        
        if self.data == "addonPrefs":
            data = context.preferences.addons[__package__].preferences
        else:
            #evaluate data so that it can be used with getattr
            data = eval(self.data)

        print(data)
        
        #get current value of toggleBool
        val = getattr(data, self.group, True)
        
        #Toggle
        setattr(data, self.group, not(val))

        return {'FINISHED'}
    # END execute()
# END Operator()

# -----------------------------------------------------------------------------
#   Toggle Relationship Lines in all 3D Views
# -----------------------------------------------------------------------------    

class VIEW3D_OT_ntzbu_toggle_relationship_lines_in_all_3dviews(Operator):
    """Tooltip"""
    bl_idname           = "view3d.ntzbu_toggle_relationship_lines_in_all_3dviews"
    bl_label            = "NTZBU : Toggle Relationship Lines in all 3D Views"
    bl_description      = "Toggle Relationship Lines in all 3D Views"

    state : BoolProperty (
        default = True,
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        #overlay = bpy.context.space_data.overlay
        for win in context.window_manager.windows:
            for area in win.screen.areas:
                if area.type == 'VIEW_3D':
                    overlay = area.spaces.active.overlay

                    overlay.show_relationship_lines = self.state
        

        return {'FINISHED'}
    # END execute()
# END Operator()
