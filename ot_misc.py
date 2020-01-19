import bpy
from . props_misc import NTZBNSUTLS_selcontigedgprops
from . import misc_functions

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#   Reset Settings
# -----------------------------------------------------------------------------    

class NTZBNSUTLS_OT_resetsettings(Operator):
    """Tooltip"""
    bl_idname = "ntzbnsutls.resetsettings"
    bl_label = "Neltulz - Bonus Utils : Reset Setting(s)"
    bl_description = "Resets setting(s)"

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

    #Modifier Visibility - Reset List
    mdfrtools_settingsToReset_List = [
        ("render",    "Render",    "", "", 1 << 2),
        ("realtime",  "Realtime",  "", "", 1 << 3),
        ("editmode",  "Edit Mode", "", "", 1 << 4),
        ("cage",      "Cage",      "", "", 1 << 5),
        ("affect",    "Affect",    "", "", 1 << 6),
        ("apply",     "Apply",     "", "", 1 << 7),
    ]

    mdfrtools_settingsToReset : EnumProperty (
        options={'ENUM_FLAG'},
        items=mdfrtools_settingsToReset_List,
        name="Modifier Visibility Setting(s) to Reset",
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

        elif self.settingsPropList == "MDFRTOOLS":
            data = scn.ntzbnsutls_mdfrtools
            propNameList = self.mdfrtools_settingsToReset

        for propName in propNameList:
            
            defaultVal = data.__annotations__[propName][1]['default']
            setattr(data, propName, defaultVal)

        propNameList.clear()

        return {'FINISHED'}
    # END execute()
# END Operator()

