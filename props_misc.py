import bpy

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (PropertyGroup)

#Neltulz - Bonus Utils Properties
class NTZBNSUTLS_props(PropertyGroup):

    show_object_section : BoolProperty (
        name="Show Object Section",
        default = True,
    )

    show_meshEditMode_section : BoolProperty (
        name="Show Mesh Edit Mode Section",
        default = True,
    )

    show_modifiers_section : BoolProperty (
        name="Show Modifiers Section",
        default = True,
    )

#Select Contiguous Edges Properties
class NTZBNSUTLS_selcontigedgprops(PropertyGroup):

    useCustomSettings_List = [
        ("UNSET",  "Unset (Use Last Known)", "Uses the last known user configured settings in the operator",    "",                  1),
        ("CUSTOM", "Custom",                 "Forces the operator to use these settings every time",            "DECORATE_OVERRIDE", 2),
    ]

    useCustomSettings : EnumProperty (
        items       = useCustomSettings_List,
        name        = "Settings",
        default     = "CUSTOM"
    )

    maxAngle : IntProperty(
        name        = "Max Angle",
        default     = 15,
        min         = 0,
        max         = 360,
    )

    maxEdges : IntProperty(
        name        = "Max Edges",
        default     = 0,
        min         = 0,
        soft_max    = 50
    )

    direction_List = (
        ('BACKWARD', "Backward", "", "", 0),
        ('BOTH',     "Both",     "", "", 1),
        ('FORWARD',  "Forward",  "", "", 2),
    )

    direction : EnumProperty(
        items			= direction_List,
        name			= "Direction",
        description		= "Search Direction",
        default			= 'BOTH',
    )

#Modifier Visibility Properties
class NTZBNSUTLS_mdfrtoolsprops(PropertyGroup):

    useCustomModifierVisibilitySettings_List = [
        ("UNSET",  "Unset (Use Last Known)", "Uses the last known user configured settings in the operator",    "",                  1),
        ("CUSTOM", "Custom",                 "Forces the operator to use these settings every time",            "DECORATE_OVERRIDE", 2),
    ]

    useCustomModifierVisibilitySettings : EnumProperty (
        items       = useCustomModifierVisibilitySettings_List,
        name        = "Settings",
        default     = "CUSTOM"
    )

    useCustomModifierApplySettings_List = [
        ("UNSET",  "Unset (Use Last Known)", "Uses the last known user configured settings in the operator",    "",                  1),
        ("CUSTOM", "Custom",                 "Forces the operator to use these settings every time",            "DECORATE_OVERRIDE", 2),
    ]

    useCustomModifierApplySettings : EnumProperty (
        items       = useCustomModifierApplySettings_List,
        name        = "Settings",
        default     = "CUSTOM"
    )

    render : BoolProperty (
        name="Render",
        description="Show/Hide Render for all modifiers",
        default = True,
    )

    realtime : BoolProperty (
        name="Realtime",
        description="Show/Hide Realtime for all modifiers",
        default = True,
    )

    editmode : BoolProperty (
        name="Edit Mode",
        description="Show/Hide Edit Mode for all modifiers",
        default = False,
    )

    cage : BoolProperty (
        name="Cage",
        description="Show/Hide Cage for all modifiers",
        default = False,
    )

    apply_List = [
        ("ONLY_VISIBLE",          "Only visible & keep hidden",       "Applies only visible modifiers.  Any hidden modifiers will be ignored, and will be kept so that you can unhide and use them later",           "", 0),
        ("VISIBLE_AND_REMOVE",    "Only visible & remove hidden",     "Applies only visible modifiers.  Any hidden modifiers will be removed.  The resulting object(s) will have no modifiers remaining",            "", 1),
        ("ALL",                   "All (Applies hidden)",             "Applies all, which is the blender default.  Any hidden modifiers will be unhidden and applied, which can be seen as unpredictable behavior",  "", 2),
    ]

    apply : EnumProperty (
        items       = apply_List,
        name        = "Apply",
        description = "Which modifiers to apply",
        default     = "VISIBLE_AND_REMOVE"
    )