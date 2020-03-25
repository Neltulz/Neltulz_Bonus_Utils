#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Name        : Smart Instance Collection
# Description : Converts Selected Objects into an Instance Collection
# Author      : Neltulz (Neil V. Moore)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import bpy
import mathutils
from . import miscFunc
from . import miscLay

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#   Smart Unparent
# -----------------------------------------------------------------------------    

class VIEW3D_OT_ntzbu_smart_instance_collection(Operator):
    """Tooltip"""
    bl_idname           = 'view3d.ntzbu_smart_instance_collection'
    bl_label            = 'NTZBU : Smart Instance Collection'
    bl_description      = 'Converts Selected Objects into an Instance Collection'
    bl_options          = {'REGISTER', 'UNDO',
    #'PRESET'
    }

    showConfirmDiag : BoolProperty (
        name            = 'Show Confirm Dialog',
        description     = 'Shows Confirmation Dialog',
        default         = False,
    )

    confirmDiagReason : StringProperty (
        name="Confirm Dialog Reason",
        description="Reason for showing the confirm dialog",
        default = '',
    )

    instCollName : StringProperty (
        name="Instance Collection Name",
        description="Name of the resulting instance collection",
        default = 'Collection',
    )

    collSceneDest : StringProperty (
        name="Scene Destination",
        description="Name of the scene for the collection of objects to go to",
        default = 'Assets',
    )

    modeAtBegin         = "OBJECT"
    cursorLocAtBegin    = None

    showOperatorOptions : BoolProperty (
        name            = 'Show Operator Options',
        description     = 'Shows additional operator options',
        default         = False,
    )

    instOrigin_List = [
        ("TFORMPIVOT",                 "Default",                                'Cursor will be placed using the user chosen "Transform Pivot Point" method',  "", 0),
        None,
        ("CURSOR",                     "3D Cursor",                              "",                                                                            "", 1),
        ("BOUNDING_BOX_CENTER",        "Bounding Box Center",                    "",                                                                            "", 2),
        ("MEDIAN_POINT",               "Median Point",                           "",                                                                            "", 3),
        ("ACTIVE_ELEMENT",             "Active Element",                         "",                                                                            "", 4),
        ("WORIGIN",                    "World Origin",                           "",                                                                            "", 5),
    ]

    instOrigin : EnumProperty (
        items       = instOrigin_List,
        name        = "Instance Pivot Location",
        default     = "TFORMPIVOT"
    )
    
    autoCollOffset : BoolProperty (
        name="Auto Collection Offset",
        description="Automatically calculate collection offset when moving objects to another scene",
        default = True,
    )
    
    offsetMargin : FloatProperty (
        name="Offset Margin",
        description="Margin between nearby objects",
        default = 10,
    )

    switchToDestScn : BoolProperty (
        name="Switch to Destination Scene",
        description="Switch to destination scene",
        default = False,
    )

    @classmethod
    def poll(cls, context):
        return (context.mode == "OBJECT") and ( len(context.selected_objects) > 0 )

    def invoke(self, context, event):
        
        selObjs = context.selected_objects

        self.confirmDiagReason = ''
        self.showConfirmDiag = False #declare
        for obj in selObjs:
            if obj.instance_type == "COLLECTION":
                self.showConfirmDiag = True
                self.confirmDiagReason = 'COLLECTION_DETECTED'
                break

        addonPrefs = context.preferences.addons[__package__].preferences
        scn = context.scene

        '''
        # BEGIN Retreive Operator properties from addon preferences
        opPropNameList = ['emptyName', 'emptyLocation', 'emptySize']
        miscFunc.retreive_op_props_from_addonPrefs(self, context, addonPrefs=addonPrefs, opPropNameList=opPropNameList, opPropPrefix='groupWithEmpty_')
        # END Retreive Operator properties from addon preferences
        '''
        
        #EXPAND properties?
        if addonPrefs.smartInstColl_showOperatorOptions == 'EXPAND':
            self.showOperatorOptions = True
        else:
            self.showOperatorOptions = False

        #store cursor location at begin
        self.cursorLocAtBegin = mathutils.Vector(scn.cursor.location)
        
        #store mode at begin
        self.modeAtBegin = context.mode

        if self.showConfirmDiag:
            return context.window_manager.invoke_props_dialog(self, width=300)
        else:
            return context.window_manager.invoke_props_dialog(self)
            #return self.execute(context)
    # END invoke()

    def draw(self, context):
        scn = context.scene
        lay = self.layout.column(align=True)



        if self.showOperatorOptions:
            box = lay.box().column(align=True)

            miscLay.createPropOLD(self, context, labelText='Origin', data=self, propItem='instOrigin', layout=box)

            box.separator()

            miscLay.createPropOLD(self, context, propText='Auto Collection Offset', data=self, propItem='autoCollOffset', layout=box)
            
            box.separator()
            
            offsetMargin_row = box.row(align=True)
            offsetMargin_row.active = self.autoCollOffset

            miscLay.createPropOLD(self, context, labelText='Offset Margin', data=self, propItem='offsetMargin', layout=offsetMargin_row)
            
            box.separator()
            
            miscLay.createPropOLD(self, context, propText='Switch to Scene', data=self, propItem='switchToDestScn', layout=box)

            

        lay.separator()

        row = lay.row(align=False)

        instCollName_col = row.column(align=True)
        labelText = instCollName_col.row(align=True)
        labelText.label(text='Collection Name:')

        instCollName_row = instCollName_col.row(align=True)
        instCollName_row.scale_y = 1.25
        instCollName_row.prop(self, 'instCollName', text='')
        

        collSceneDest_col = row.column(align=True)
        collSceneDest_col.label(text='Scene Name:')

        collSceneDest_row = collSceneDest_col.row(align=True)
        collSceneDest_row.scale_y = 1.25
        collSceneDest_row.prop(self, 'collSceneDest', text='')


        optionsShowHide_row = row.column(align=True)
        optionsShowHide_row.scale_y = 1
        optionsShowHide_row.label(text='', icon="BLANK1")

        vSpacer = optionsShowHide_row.row(align=True)
        vSpacer.scale_y = 1

        if self.showOperatorOptions:    icon = 'TRIA_UP'
        else:                           icon = 'TRIA_RIGHT'

        optionsShowHide_btn = optionsShowHide_row.row(align=True)
        optionsShowHide_btn.scale_y = 1.25
        optionsShowHide_btn.prop(self, 'showOperatorOptions', text='', icon=icon)

        if self.showConfirmDiag:

            if self.confirmDiagReason == 'COLLECTION_DETECTED':

                lay.separator()

                numSelObjs = len(context.selected_objects)

                box = lay.box().column(align=True)

                box.separator()

                row = box.row(align=True)
                
                icon = row.column(align=True)
                icon.scale_y = 1.5
                icon.ui_units_x = 2
                miscLay.forceJustifyText(lay=icon, text='', icon='ERROR', alignment='RIGHT')
                
                row.separator()

                paragraph = row.column(align=True)
                paragraph.scale_y = 0.75

                if numSelObjs == 1:
                    miscLay.forceJustifyText(lay=paragraph, text='The selected object is an', alignment='LEFT')
                    miscLay.forceJustifyText(lay=paragraph, text='"Instance Collection"', alignment='LEFT')

                else:
                    miscLay.forceJustifyText(lay=paragraph, text='One (or more) of the selected', alignment='LEFT')
                    miscLay.forceJustifyText(lay=paragraph, text='objects is an "Instance Collection"', alignment='LEFT')

                box.separator()

    # END draw()

    

    def execute(self, context):

        self.showConfirmDiag = False #reset
        self.confirmDiagReason = '' #reset

        if context.mode == "OBJECT":

            # BEGIN ensure one of the selected objects is an active object
            # ------------------------------------------------------------
            activeObjAtBegin = context.view_layer.objects.active
            selObjs = context.selected_objects

            if len(selObjs) > 0:
                if (activeObjAtBegin is None) or (not activeObjAtBegin in selObjs):
                    context.view_layer.objects.active = selObjs[0]
                    activeObjAtBegin = selObjs[0]
            # ------------------------------------------------------------
            # END ensure active obj

         
            scn = context.scene
                       
            # BEGIN Snap Cursor Based on 'self.instOrigin'
            # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            tformPivotAtBegin = str(scn.tool_settings.transform_pivot_point)

            if self.instOrigin == "TFORMPIVOT":
                
                if tformPivotAtBegin == "BOUNDING_BOX_CENTER":
                    miscFunc.snapCursorToBoundingBoxCenter(self, context, activeObj=activeObjAtBegin, objMode=self.modeAtBegin, tformPivotPoint=tformPivotAtBegin)

                elif tformPivotAtBegin == "MEDIAN_POINT":
                    miscFunc.snapCursorToMedianPoint(self, context, activeObj=activeObjAtBegin, objMode=self.modeAtBegin, tformPivotPoint=tformPivotAtBegin)

                elif tformPivotAtBegin == "ACTIVE_ELEMENT":
                    bpy.ops.view3d.snap_cursor_to_active()

                elif tformPivotAtBegin == "CURSOR":
                    pass

                else:
                    miscFunc.snapCursorToMedianPoint(self, context, activeObj=activeObjAtBegin, objMode=self.modeAtBegin, tformPivotPoint=tformPivotAtBegin) #all other situations (e.g. individual origins, cursor, etc)

            elif self.instOrigin == "DEFAULT":
                bpy.ops.view3d.snap_cursor_to_selected()

            elif self.instOrigin == "BOUNDING_BOX_CENTER":
                scn.tool_settings.transform_pivot_point = self.instOrigin
                miscFunc.snapCursorToBoundingBoxCenter(self, context, activeObj=activeObjAtBegin, objMode=self.modeAtBegin, tformPivotPoint=tformPivotAtBegin)
                scn.tool_settings.transform_pivot_point = tformPivotAtBegin #reset

            elif self.instOrigin == "MEDIAN_POINT":
                scn.tool_settings.transform_pivot_point = self.instOrigin
                miscFunc.snapCursorToMedianPoint(self, context, activeObj=activeObjAtBegin, objMode=self.modeAtBegin, tformPivotPoint=tformPivotAtBegin)
                scn.tool_settings.transform_pivot_point = tformPivotAtBegin #reset

            elif self.instOrigin == "ACTIVE_ELEMENT":
                scn.tool_settings.transform_pivot_point = self.instOrigin
                bpy.ops.view3d.snap_cursor_to_active()
                scn.tool_settings.transform_pivot_point = tformPivotAtBegin #reset

            elif self.instOrigin == "WORIGIN":
                scn.cursor.location = (0,0,0)
            # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            # END Snap Cursor Based on 'self.instOrigin'
            
            #check if destination scene already exists
            destScn = None #declare
            for scn in bpy.data.scenes:
                if scn.name == self.collSceneDest:
                    destScn = scn

            if destScn is None:
                #create a new scene with user specified name
                destScn = bpy.data.scenes.new(name=self.collSceneDest)

            #create a new collection in the new scene with user specified name
            newColl = bpy.data.collections.new(self.instCollName)
            destScn.collection.children.link(newColl)


            context.window.scene = destScn #switch to destination scene
            destObjs = [] #declare
            for obj in destScn.objects:
                destObjs.append(obj)
                obj.select_set(False)
            context.window.scene = scn #switch back to original scene



            totalCollOffsetVec = mathutils.Vector( (0, 0, 0) ) #declare
            if self.autoCollOffset:

                #calculate dimension of selected objects
                selDim = miscFunc.max_dim_from_objs_or_empties(self, context, minMaxAvg='MAX', objs=selObjs)
                
                destDim = 0 #declare
                if destObjs != []:
                    #calculate dimension of objects in the destination scene
                    destDim = miscFunc.max_dim_from_objs_or_empties(self, context, minMaxAvg='MAX', objs=destObjs)
                
                #create vector from dimension of objects in the destination scene
                destDimVec = mathutils.Vector( (destDim, 0, 0) )


                
                #create vector from offset Margin
                if destDim > 0:
                    offsetMarginVec = mathutils.Vector( (self.offsetMargin, 0, 0) )
                else:
                    offsetMarginVec = mathutils.Vector( (0, 0, 0) )

                #add the two together to create a total offset vector
                totalCollOffsetVec = destDimVec + offsetMarginVec


            for obj in selObjs:
                #move objects to the origin, and then offset them by their own object location minus the 3D cursor location, and then offset the objects so that they do not overlap any existing objects in the scene
                obj.location = mathutils.Vector( (0,0,0) ) + ( obj.location - scn.cursor.location ) + totalCollOffsetVec
                
                #find all collections that the obj is currently linked to
                objColls = obj.users_collection

                #link selected object to the new collection in the new scene
                newColl.objects.link(obj)

                #unlink the object from all of the collections it's currently linked to
                for objColl in objColls:
                    objColl.objects.unlink(obj)
                

            #set instance collection offset so that the origin ends up where the user wanted it
            newColl.instance_offset = totalCollOffsetVec

            #create an instance collection of the selected objects in the original place of the selected objects
            bpy.ops.object.collection_instance_add(collection=newColl.name, location=scn.cursor.location)

            if self.switchToDestScn:
                context.window.scene = destScn
                bpy.ops.view3d.view_all('INVOKE_DEFAULT', use_all_regions=True)



            scn.cursor.location = self.cursorLocAtBegin #reset


        else:
            self.report({'INFO'}, 'Unsupported mode detected.  Please use "Object Mode".' )
        

        return {'FINISHED'}
    # END execute()
# END Operator()
