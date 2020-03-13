#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Name        : Group With Empty
# Description : Parent a selection of objects to an invisible empty so that they may be moved/rotated/scaled similar to how Autodesk Maya groups objects
# Author      : Neltulz (Neil V. Moore)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import ctypes
import bpy
import mathutils
from . import miscFunc

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Operator)

class VIEW3D_OT_ntzbu_group_with_empty(Operator):
    """Tooltip"""
    bl_idname           = "view3d.ntzbu_group_with_empty"
    bl_label            = "NTZBU : Group With Empty"
    bl_description      = "Parent a selection of objects to an invisible empty so that they may be moved/rotated/scaled similar to how Autodesk Maya groups objects"
    bl_options          = {'REGISTER', 'UNDO'}

    modeAtBegin         = "OBJECT"
    selObjNames         = []
    cursorLocAtBegin    = None
    activeObjName       = None

    showOperatorOptions : BoolProperty (
        name            = 'Show Operator Options',
        description     = 'Shows additional operator options',
        default         = False,
    )

    emptyLocation_List = [
        ("MEDIAN_POINT",             "Median",         "Median Point",          "", 0),
        ("BOUNDING_BOX_CENTER",      "Bounding",       "Bounding Box Center",   "", 1),
        ("ACTIVE_ELEMENT",           "Active",         "Active Element",        "", 2),
        ("WORIGIN",                  "Origin",         "World Orign",           "", 3),
    ]

    emptyLocation : EnumProperty (
        items       = emptyLocation_List,
        name        = "Empty Location",
        default     = "MEDIAN_POINT",
    )

    emptyName : StringProperty (
        default     = "Group",
    )

    emptySize_List = [
        ("1",      "1",         "",   "", 0),
        ("0.01",   "0.01",      "",   "", 1),
        ("0.0001", "0.0001",    "",   "", 2),
    ]

    emptySize : EnumProperty (
        items       = emptySize_List,
        name        = "Empty Location",
        default     = "0.0001",
    )

    @classmethod
    def poll(cls, context):
        return (context.mode == "OBJECT") and ( len(context.selected_objects) > 0 )

    def invoke(self, context, event):

        addonPrefs = context.preferences.addons[__package__].preferences

        scn = context.scene

        if addonPrefs.groupWithEmpty_showOperatorOptions == 'EXPAND':
            self.showOperatorOptions = True
        else:
            self.showOperatorOptions = False

        self.cursorLocAtBegin = mathutils.Vector(scn.cursor.location)
        
        self.modeAtBegin = context.mode

        self.selObjNames.clear()
        for obj in bpy.context.selected_objects:
            self.selObjNames.append(obj.name)

        return self.execute(context)
    # END invoke()

    def draw(self, context):
        lay = self.layout.column(align=True)

        if self.showOperatorOptions:
            box = lay.box().column(align=True)

            box.label(text="Empty Location:")
            row = box.row(align=True)
            row.prop(self, 'emptyLocation', expand=True)

            box.separator()

            box.label(text="Empty Size:")
            row = box.row(align=True)
            row.prop(self, 'emptySize', expand=True)

            lay.separator()

        row = lay.row(align=True)
        row.scale_y = 1.25
        row.prop(self, 'emptyName', text='')

        row.separator()

        if self.showOperatorOptions:
            icon = 'TRIA_UP'
        else:
            icon = 'TRIA_RIGHT'

        row.prop(self, 'showOperatorOptions', text='', icon=icon)


    # END draw()

    def execute(self, context):
        #ensure one of the selected objects is an active object
        if context.view_layer.objects.active is None:
            if len(context.selected_objects) > 0:
                context.view_layer.objects.active = context.selected_objects[0]

        #store name of active object
        self.activeObjName = f'{context.view_layer.objects.active.name}'

        #store scn
        scn = context.scene

        #if mode is 'OBJECT'
        if self.modeAtBegin == 'OBJECT':

            #store name of current transform pivot location (e.g. MEDIAN_POINT, BOUNDING_BOX_CENTER, etc)
            tformPivotAtBegin = f'{scn.tool_settings.transform_pivot_point}'


            #if empty location is median or bounding, change "transform pivot" to median or bounding, snap cursor, then reset "transform pivot"
            if self.emptyLocation in ['MEDIAN_POINT', 'BOUNDING_BOX_CENTER', 'ACTIVE_ELEMENT']:
                scn.tool_settings.transform_pivot_point = self.emptyLocation #set pivot transform to emptyLocation

                if self.emptyLocation in ['MEDIAN_POINT', 'BOUNDING_BOX_CENTER']:
                    bpy.ops.view3d.snap_cursor_to_selected() #snap cursor to selected

                elif self.emptyLocation == 'ACTIVE_ELEMENT':
                    bpy.ops.view3d.snap_cursor_to_active() #snap cursor to active

                scn.tool_settings.transform_pivot_point = tformPivotAtBegin #reset pivot transform

            

            #create empty with custom name and link it to the scene
            newEmpty = bpy.data.objects.new(self.emptyName, None)
            bpy.context.collection.objects.link(newEmpty)

            #set location of the newly created empty according to the "emptyLocation" operator property
            if self.emptyLocation in ['MEDIAN_POINT', 'BOUNDING_BOX_CENTER', 'ACTIVE_ELEMENT']:
                newEmpty.location = scn.cursor.location

            elif self.emptyLocation == 'WORIGIN':
                newEmpty.location = (0,0,0)
            
            #set empty display size
            newEmpty.empty_display_size = eval(self.emptySize)

            #store the parent of the active object if one exists
            childObjLastParent = context.view_layer.objects.active.parent

            #clear parents and keep transform of all of the selected objects
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

            #parent the objects to the newly created empty
            for childObjName in self.selObjNames:
                childObj = bpy.data.objects[childObjName]

                childObj.parent = newEmpty
                childObj.matrix_parent_inverse = newEmpty.matrix_world.inverted()
            
            #if the active object at begin had a parent, then the newly created empty must be parented to its old parent
            if childObjLastParent is not None:
                newEmpty.parent = childObjLastParent
                newEmpty.matrix_parent_inverse = childObjLastParent.matrix_world.inverted()
            
            #reset cursor location
            scn.cursor.location = self.cursorLocAtBegin

        else:
            self.report({'INFO'}, 'Unsupported mode detected.  Please use "Object Mode".' )
        
        
        return {'FINISHED'}
    # END execute()


# END Operator()