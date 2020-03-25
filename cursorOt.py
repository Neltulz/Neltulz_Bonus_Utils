
import bpy
import bmesh
import numpy as np
from mathutils      import Matrix
from mathutils      import Euler
from mathutils      import Vector
from math           import radians
from .              import miscFunc
from .              import miscLay

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Name        : Adjust 3D Cursor
# Description : Adds an empty at the location of the 3D cursor, which the user can move/rotate before applying
# Author      : Neltulz (Neil V. Moore)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class VIEW3D_OT_ntzbu_adjust_3d_cursor(Operator):
    bl_idname           = "view3d.ntzbu_adjust_3d_cursor"
    bl_label            = "NTZBU : Adjust 3D Cursor"
    bl_description      = "Adds an empty at the location of the 3D cursor, which the user can move/rotate before applying"
    bl_options          = {'REGISTER', 'UNDO',
    #'PRESET'
    }
    
    emptyDisplayType_list = [
        ("PLAIN_AXES"       ,    "Plain Axes"       ,     "",     "EMPTY_AXIS"          ,     0),
        ("ARROWS"           ,    "Arrows"           ,     "",     "EMPTY_ARROWS"        ,     1),
        ("SINGLE_ARROW"     ,    "Single Arrow"     ,     "",     "EMPTY_SINGLE_ARROW"  ,     2),
        ("CIRCLE"           ,    "Circle"           ,     "",     "MESH_CIRCLE"         ,     3),
        ("CUBE"             ,    "Cube"             ,     "",     "CUBE"                ,     4),
        ("SPHERE"           ,    "Sphere"           ,     "",     "SPHERE"              ,     5),
        ("CONE"             ,    "Cone"             ,     "",     "CONE"                ,     6),
        ("IMAGE"            ,    "Image"            ,     "",     "IMAGE_DATA"          ,     7),
    ]

    emptyDisplayType : EnumProperty (
        items       = emptyDisplayType_list,
        name        = "Display As",
        description = "Change the display of the empty",
        default     = "PLAIN_AXES",
    )

    size : FloatProperty (
        name        = "Size",
        description = "Change the size of the empty",
        default     = 0.25,
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scn = context.scene
        cursorLoc = scn.cursor.location
        cursorRot = scn.cursor.rotation_euler

        scn.cursor.rotation_mode = 'XYZ'

        cursorAdjustEmpty = bpy.data.objects.get("NTZBNSUTLS_CursorAdjust")

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

        if cursorAdjustEmpty is None:
            bpy.ops.object.empty_add(type=self.emptyDisplayType, radius=self.size, align='CURSOR', location=cursorLoc)
            cursorAdjustEmpty = context.view_layer.objects.active
            cursorAdjustEmpty.name = 'NTZBNSUTLS_CursorAdjust'

            cursorAdjustEmpty.rotation_mode = 'XYZ'
        else:
            bpy.context.view_layer.objects.active = cursorAdjustEmpty
            cursorAdjustEmpty.select_set(True)
            cursorAdjustEmpty.location = cursorLoc
            cursorAdjustEmpty.rotation_euler = cursorRot
            cursorAdjustEmpty.empty_display_type = self.emptyDisplayType
            cursorAdjustEmpty.empty_display_size = self.size

        return {'FINISHED'}
    #END execute()

    
    def draw(self, context):
        scn = context.scene
        lay = self.layout.column(align=True)

        obj = context.object

        miscLay.createPropOLD(self, context, labelText='Display As', data=self, propItem='emptyDisplayType', layout=lay)

        lay.separator()

        miscLay.createPropOLD(self, context, labelText='Size', data=self, propItem='size', layout=lay)

    #END draw()

#END Operator()

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Name        : Apply 3D Cursor
# Description : Updates the location/rotation of the 3D Cursor from a temporary empty
# Author      : Neltulz (Neil V. Moore)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class VIEW3D_OT_ntzbu_apply_3d_cursor(Operator):
    bl_idname           = "view3d.ntzbu_apply_3d_cursor"
    bl_label            = "NTZBU : Apply 3D Cursor"
    bl_description      = "Updates the location/rotation of the 3D Cursor from a temporary empty"
    bl_options          = {'REGISTER', 'UNDO',
    #'PRESET'
    }

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scn = context.scene

        try:
            #try to determine objectMode
            objModeAtBegin = bpy.context.object.mode
        except:
            objModeAtBegin = "OBJECT"

        scn.cursor.rotation_mode = 'XYZ'

        cursorAdjustEmpty = bpy.data.objects.get("NTZBNSUTLS_CursorAdjust")

        if cursorAdjustEmpty is not None:

            bpy.ops.object.mode_set(mode='OBJECT')

            activeObjAtBegin = bpy.context.view_layer.objects.active

            selObjs = context.selected_objects

            bpy.ops.object.select_all(action='DESELECT')

            bpy.context.view_layer.objects.active = cursorAdjustEmpty
            cursorAdjustEmpty.select_set(True)

            cursorAdjustEmpty.rotation_mode = 'XYZ'

            bpy.ops.view3d.snap_cursor_to_selected()
            scn.cursor.rotation_euler = cursorAdjustEmpty.rotation_euler

            bpy.context.view_layer.objects.active = activeObjAtBegin

            for obj in selObjs:
                obj.select_set(True)

            bpy.data.objects.remove(cursorAdjustEmpty)

            if objModeAtBegin == 'EDIT':
                bpy.ops.object.mode_set(mode='EDIT')
        
        return {'FINISHED'}
    #END execute()


#END Operator()


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Name        : Rotate 3D Cursor
# Description : Adds an empty at the location of the 3D cursor, which the user can move/rotate before applying
# Author      : iceythe (Kaio)
# Permission  : Special thanks to iceythe for the creation of this script and permission to include it with the Neltulz - Bonus Utils add-on
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class VIEW3D_OT_ntzbu_rotate_3d_cursor(Operator):
    bl_idname           = "view3d.ntzbu_rotate_3d_cursor"
    bl_label            = "NTZBU : Rotate 3D Cursor"
    bl_description      = "Rotate 3D Cursor"
    bl_options          = {'REGISTER', 'UNDO',
    #'PRESET'
    }
    xyz: bpy.props.FloatVectorProperty(size=3, min=-180, max=180)

    def execute(self, context):
        # Cursor matrix
        cmat = self.cmat.copy()

        # Local rotation matrix
        mat = Euler((radians(angle) for angle in self.xyz)).to_matrix()

        # Multiply with inverse local rotation matrix
        new_mat = cmat @ mat.inverted()

        context.scene.cursor.rotation_quaternion = new_mat.to_quaternion()
        return {'FINISHED'}
    #END execute()

    def invoke(self, context, event):
        context.scene.cursor.rotation_mode = 'QUATERNION'
        self.cmat = context.scene.cursor.rotation_quaternion.to_matrix()
        return self.execute(context)
    #END invoke()

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "xyz", slider=True)
    #END draw()

#END Operator()


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Name        : Snap Cursor+
# Description : Snaps cursor to selected with orientation
# Author      : Neltulz (Neil V. Moore)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class VIEW3D_OT_ntzbu_snap_cursor_plus(Operator):
    bl_idname           = "view3d.ntzbu_snap_cursor_plus"
    bl_label            = "NTZBU : Snap Cursor+"
    bl_description      = "Snaps cursor to selected with orientation"
    bl_options          = {'REGISTER', 'UNDO',
    #'PRESET'
    }

    cursorLocationAtInvoke : FloatVectorProperty (
        name="Cursor Location at Invoke"
    )

    cursorRotationAtInvoke : FloatVectorProperty (
        name="Cursor Rotation at Invoke"
    )

    useLocation : BoolProperty (
        name="Use Location",
        default = True,
    )
    
    location_List = [
        ("TFORMPIVOT",                 "Default",                                'Cursor will be placed using the user chosen "Transform Pivot Point" method',  "", 0),
        None,
        ("BOUNDING_BOX_CENTER",        "Bounding Box Center",                    "",                                                                            "", 2),
        ("MEDIAN_POINT",               "Median Point",                           "",                                                                            "", 3),
        ("ACTIVE_ELEMENT",             "Active Element",                         "",                                                                            "", 4),
        ("WORIGIN",                    "World Origin",                           "",                                                                            "", 5),
    ]

    location : EnumProperty (
        items       = location_List,
        name        = "Location",
        default     = "TFORMPIVOT"
    )

    useOrientation : BoolProperty (
        name="Use Orientation",
        default = True,
    )

    useCustomSettings_List = [
        ("TFORMORIENT",   "Default",                                "Orientation will be set to the user chosen Transform Orientation", "", 0),
        None,
        ("GLOBAL",        "Global",                                 "",                                                                 "", 1),
        ("LOCAL",         "Local",                                  "",                                                                 "", 2),
        ("NORMAL",        "Normal",                                 "",                                                                 "", 3),
        ("VIEW",          "View",                                   "",                                                                 "", 4),
    ]

    orientation : EnumProperty (
        items       = useCustomSettings_List,
        name        = "Orientation",
        default     = "TFORMORIENT"
    )



    def draw(self, context):
        scn = context.scene
        lay = self.layout.column(align=True)

        
        row = lay.row(align=True)
        row.prop(self, 'useLocation')

        locationRow = row.row(align=True)
        if not self.useLocation:
            locationRow.enabled = False
        locationRow.prop(self, 'location', text='')

        lay.separator()

        row = lay.row(align=True)
        row.prop(self, 'useOrientation')

        orientationRow = row.row(align=True)
        if not self.useOrientation:
            orientationRow.enabled = False
        orientationRow.prop(self, 'orientation', text='')

    #END draw()

    @classmethod
    def poll(cls, context):

        return True

    def execute(self, context):
        scn = context.scene
        
        try:
            #try to determine objectMode
            objModeAtBegin = bpy.context.object.mode
        except:
            objModeAtBegin = "OBJECT"

        activeObjAtBegin = bpy.context.view_layer.objects.active
        selObjs = context.selected_objects
        numObjsWithVertsSel = 0 #declare


        if objModeAtBegin == "OBJECT":
            
            #if there is no active object, yet there are selected objects, ensure the first selected object becomes the active object
            if (activeObjAtBegin == None) or (not activeObjAtBegin in selObjs):
                if len(selObjs) > 0:
                    activeObjAtBegin = selObjs[0]
                    bpy.context.view_layer.objects.active = activeObjAtBegin

        elif objModeAtBegin == "EDIT":

            if activeObjAtBegin.type == "MESH":

                #determine number of objects with vertex selections, and create a list with only those objects
                objsWithVertSel = set() #declare
                for obj in selObjs:

                    if obj.type == "MESH":
                        
                        bm = bmesh.from_edit_mesh(obj.data)
                        v = [v for v in bm.verts if v.select]
                        if len(v) > 0:
                            numObjsWithVertsSel += 1
                            objsWithVertSel.add(obj)

                if numObjsWithVertsSel >= 1:
                    
                    if activeObjAtBegin not in objsWithVertSel:

                        activeObjAtBegin = next(iter(objsWithVertSel)) #make the first object the active object
                        bpy.context.view_layer.objects.active = activeObjAtBegin



        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # 3D Cursor Location
        #-----------------------------------------------------------------------------------------------------------------------------------------------

        if self.useLocation:

            tformPivotAtBegin = str(scn.tool_settings.transform_pivot_point)

            if self.location == "TFORMPIVOT":
                
                if tformPivotAtBegin == "BOUNDING_BOX_CENTER":
                    miscFunc.snapCursorToBoundingBoxCenter(self, context, activeObj=activeObjAtBegin, objMode=objModeAtBegin, tformPivotPoint=tformPivotAtBegin, numObjsWithVertsSel=numObjsWithVertsSel)

                elif tformPivotAtBegin == "MEDIAN_POINT":
                    miscFunc.snapCursorToMedianPoint(self, context, activeObj=activeObjAtBegin, objMode=objModeAtBegin, tformPivotPoint=tformPivotAtBegin)

                elif tformPivotAtBegin == "ACTIVE_ELEMENT":
                    bpy.ops.view3d.snap_cursor_to_active()

                else:
                    miscFunc.snapCursorToMedianPoint(self, context, activeObj=activeObjAtBegin, objMode=objModeAtBegin, tformPivotPoint=tformPivotAtBegin) #all other situations (e.g. individual origins, cursor, etc)

            elif self.location == "DEFAULT":
                bpy.ops.view3d.snap_cursor_to_selected()

            elif self.location == "BOUNDING_BOX_CENTER":
                scn.tool_settings.transform_pivot_point = self.location
                miscFunc.snapCursorToBoundingBoxCenter(self, context, activeObj=activeObjAtBegin, objMode=objModeAtBegin, tformPivotPoint=tformPivotAtBegin, numObjsWithVertsSel=numObjsWithVertsSel)
                scn.tool_settings.transform_pivot_point = tformPivotAtBegin #reset

            elif self.location == "MEDIAN_POINT":
                scn.tool_settings.transform_pivot_point = self.location
                miscFunc.snapCursorToMedianPoint(self, context, activeObj=activeObjAtBegin, objMode=objModeAtBegin, tformPivotPoint=tformPivotAtBegin)
                scn.tool_settings.transform_pivot_point = tformPivotAtBegin #reset

            elif self.location == "ACTIVE_ELEMENT":
                scn.tool_settings.transform_pivot_point = self.location
                bpy.ops.view3d.snap_cursor_to_active()
                scn.tool_settings.transform_pivot_point = tformPivotAtBegin #reset

            elif self.location == "WORIGIN":
                scn.cursor.location = (0,0,0)

        else:
            scn.cursor.location = self.cursorLocationAtInvoke

        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # 3D Cursor Orientation
        #-----------------------------------------------------------------------------------------------------------------------------------------------

        if self.useOrientation:
            
            rotationModeAtBegin = context.scene.cursor.rotation_mode #store so it can be reset later
            #Force rotation_mode to be XYZ in case the user changed it or another add-on changed it
            context.scene.cursor.rotation_mode = 'XYZ'

            transformOrientation = scn.transform_orientation_slots[0]

            cursorRot = (0,0,0) #declare


            def getLocalRotFromActiveObj():
                return activeObjAtBegin.rotation_euler

            def getRotFromNormal():
                originalOrientation = transformOrientation.type

                transformOrientation.type = "NORMAL"

                #create custom orientation
                bpy.ops.transform.create_orientation(name="NTZBNSUTLS_SNPCRSRPLS", use_view=False, use=True, overwrite=True)

                custom_orientation = transformOrientation.custom_orientation
                rotation_of_custom_orientation = custom_orientation.matrix.to_euler()[:]
                
                #delete custom orientation
                bpy.ops.transform.delete_orientation()

                #restore original orientation
                try:
                    transformOrientation.type = originalOrientation
                except:
                    pass

                return rotation_of_custom_orientation

            def getRotFromView():
                originalOrientation = transformOrientation.type

                #create custom orientation
                bpy.ops.transform.create_orientation(name="NTZBNSUTLS_SNPCRSRPLS", use_view=True, use=True, overwrite=True)

                custom_orientation = transformOrientation.custom_orientation
                rotation_of_custom_orientation = custom_orientation.matrix.to_euler()[:]
                
                #delete custom orientation
                bpy.ops.transform.delete_orientation()

                #restore original orientation
                try:
                    transformOrientation.type = originalOrientation
                except:
                    pass

                return rotation_of_custom_orientation


            if self.orientation == "TFORMORIENT":
                
                if transformOrientation.type == "LOCAL":
                    cursorRot = getLocalRotFromActiveObj()

                elif transformOrientation.type == "NORMAL":
                    cursorRot = getRotFromNormal()

                elif transformOrientation.type == "VIEW":
                    cursorRot = getRotFromView()


            elif self.orientation == "LOCAL":
                cursorRot = getLocalRotFromActiveObj()

            elif self.orientation == "NORMAL":
                cursorRot = getRotFromNormal()

            elif self.orientation == "VIEW":
                cursorRot = getRotFromView()
            
            scn.cursor.rotation_euler = cursorRot

            context.scene.cursor.rotation_mode = rotationModeAtBegin #reset
                
        else:
            scn.cursor.rotation_euler = self.cursorRotationAtInvoke

        
        return {'FINISHED'}
    #END execute()


    def invoke(self, context, event):
        scn = context.scene
        self.cursorLocationAtInvoke = scn.cursor.location
        self.cursorRotationAtInvoke = scn.cursor.rotation_euler

        return self.execute(context)
    #END invoke()

#END Operator()
