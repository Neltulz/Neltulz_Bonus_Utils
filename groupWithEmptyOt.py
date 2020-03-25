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

    bUseOverridesFromAddonPrefs : BoolProperty(
        name="Use Overrides from Add-on Preferences",
        description='Gets operator properties from the addon-preferences.  This will override any settings in the user customized keymap.  If you want to prevent the addon preferences from setting your operator properties, set this to False',
        default = True
    )

    modeAtBegin         = "OBJECT"
    selObjNames         = []
    cursorLocAtBegin    = None
    activeObjName       = None

    showOperatorOptions : BoolProperty (
        name            = 'Show Operator Options',
        description     = 'Shows additional operator options',
        default         = False,
    )

    reset_emptyName : BoolProperty( name = 'Reset "Empty Name"', default = False )
    emptyName : StringProperty (
        name        = 'Empty Name',
        default     = 'Group',
    )

    emptyLocation_List = [
        ("MEDIAN_POINT",             "Median",         "Median Point",          "", 0),
        ("BOUNDING_BOX_CENTER",      "Bound",          "Bounding Box Center",   "", 1),
        ("ACTIVE_ELEMENT",           "Active",         "Active Element",        "", 2),
        ("WORIGIN",                  "Origin",         "World Orign",           "", 3),
    ]

    reset_emptyLocation : BoolProperty( name = 'Reset "Empty Location"', default = False )
    emptyLocation : EnumProperty (
        items       = emptyLocation_List,
        name        = "Empty Location",
        default     = "MEDIAN_POINT",
    )

    emptySize_List = [
        ("1",      "1",         "",   "", 0),
        ("0.01",   "0.01",      "",   "", 1),
        ("0.0001", "0.0001",    "",   "", 2),
    ]

    reset_emptySize : BoolProperty( name = 'Reset "Empty Size"', default = False )
    emptySize : EnumProperty (
        items       = emptySize_List,
        name        = "Empty Location",
        default     = "0.01",
    )

    @classmethod
    def poll(cls, context):
        return (context.mode == "OBJECT") and ( len(context.selected_objects) > 0 )

    def invoke(self, context, event):

        addonPrefs = context.preferences.addons[__package__].preferences
        scn = context.scene

        # BEGIN Retreive Operator properties from addon preferences
        opPropNameList = ['emptyName', 'emptyLocation', 'emptySize']
        miscFunc.retreive_op_props_from_addonPrefs(self, context, addonPrefs=addonPrefs, opPropNameList=opPropNameList, opPropPrefix='groupWithEmpty_')
        # END Retreive Operator properties from addon preferences
        
        #EXPAND properties?
        if addonPrefs.groupWithEmpty_showOperatorOptions == 'EXPAND':
            self.showOperatorOptions = True
        else:
            self.showOperatorOptions = False

        #store cursor location at begin
        self.cursorLocAtBegin = mathutils.Vector(scn.cursor.location)
        
        #store mode at begin
        self.modeAtBegin = context.mode

        #store names of selected objects at begin
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
            emptyLocation_row = box.row(align=True)
            emptyLocation_row.prop(self, "emptyLocation", expand=True)
            emptyLocation_row.separator()
            resetBtn = emptyLocation_row.row(align=True)
            resetBtn.active = False
            resetBtn.prop(self, "reset_emptyLocation", toggle=True, text="", icon="LOOP_BACK", emboss=False)

            box.separator()

            box.label(text="Empty Size:")
            emptySize_row = box.row(align=True)
            emptySize_row.prop(self, "emptySize", expand=True)
            emptySize_row.separator()
            resetBtn = emptySize_row.row(align=True)
            resetBtn.active = False
            resetBtn.prop(self, "reset_emptySize", toggle=True, text="", icon="LOOP_BACK", emboss=False)

            lay.separator()


        emptyName_row = lay.row(align=True)
        emptyName_row.scale_y = 1.25
        emptyName_row.prop(self, "emptyName", text='')
        emptyName_row.separator()
        resetBtn = emptyName_row.row(align=True)
        resetBtn.active = False
        resetBtn.prop(self, "reset_emptyName", toggle=True, text="", icon="LOOP_BACK", emboss=False)

        emptyName_row.separator()

        if self.showOperatorOptions:
            icon = 'TRIA_UP'
        else:
            icon = 'TRIA_RIGHT'

        emptyName_row.prop(self, 'showOperatorOptions', text='', icon=icon)


    # END draw()

    def execute(self, context):
        
        # BEGIN Reset props if user clicked any "Reset" button in the operator adjustment panel at the lower left corner of the 3d viewport
        # ------------------------------------------------------------------------------------------------------------------------------------
        propsToReset = [
            ["reset_emptyName",         ["emptyName"]       ],
            ["reset_emptyLocation",     ["emptyLocation"]   ],
            ["reset_emptySize",         ["emptySize"]       ],
        ]

        miscFunc.resetOperatorProps(self, context, propsToReset)
        # ------------------------------------------------------------------------------------------------------------------------------------
        # END Reset props
        
        addonPrefs = context.preferences.addons[__package__].preferences
        scn = context.scene

        # BEGIN ensure one of the selected objects is an active object
        # ------------------------------------------------------------
        activeObj = context.view_layer.objects.active
        selObjs = context.selected_objects

        if len(selObjs) > 0:
            if (activeObj is None) or (not activeObj in selObjs):
                context.view_layer.objects.active = selObjs[0]
        # ------------------------------------------------------------
        # END ensure active obj



        #store name of active object
        self.activeObjName = f'{context.view_layer.objects.active.name}'


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
            newEmpty.empty_display_size = float(self.emptySize)

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

            '''
            # NOTE: CURRENTLY BROKEN/NOT WORKING AND DON'T KNOW WHY.
            #    Find and Expand selected objects in each outliner
            # -----------------------------------------------------------------------------

            # expand outliner
            activeObj = context.view_layer.objects.active
            miscFunc.expand_selected_objs_in_outliner(self, context, selObjs=[activeObj], activeObj=activeObj)
            '''
            
            #reset cursor location
            scn.cursor.location = self.cursorLocAtBegin

        else:
            self.report({'INFO'}, 'Unsupported mode detected.  Please use "Object Mode".' )
        

        return {'FINISHED'}
    # END execute()


# END Operator()