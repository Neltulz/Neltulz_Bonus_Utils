import bpy

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (PropertyGroup)

#Neltulz - Bonus Utils Properties
class ntzbu_props(PropertyGroup):

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

    show_3dcursor_section : BoolProperty (
        name="Show 3D Cursor Section",
        default = True,
    )

