import bpy
from . import miscFunc

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#   Smart Unparent
# -----------------------------------------------------------------------------    

class VIEW3D_OT_ntzbu_smart_unparent(Operator):
    """Tooltip"""
    bl_idname           = 'view3d.ntzbu_smart_unparent'
    bl_label            = 'NTZBU : Smart Unparent'
    bl_description      = 'Unparents an object while retaining hierarchy'
    bl_options          = {'REGISTER', 'UNDO',
    #'PRESET'
    }
    

    unparentMethod_List = [
        ('ONELEVEL',         'One Level',         '',      '', 1),
        ('CLEAR',            'Clear to Root',     '',      '', 0),
    ]

    unparentMethod : EnumProperty (
        items       = unparentMethod_List,
        name        = 'Parent Objects To',
        default     = 'ONELEVEL',
    )
    

    unparentType_List = [
        ('KEEPTFORM',         'Keep Tform',          'Keep Transform',      '', 1),
        ('UNPARENT',          'Unparent',            'Unparent',            '', 0),
        ('INVERSE',           'Inverse',             'Inverse',             '', 2),
    ]

    unparentType : EnumProperty (
        items       = unparentType_List,
        name        = 'Unparent Type',
        default     = 'KEEPTFORM',
    )
    
    delOrphanEmptyParents : BoolProperty (
        name        = 'Delete Orphaned Empty Parents',
        default     = True,

    )

    @classmethod
    def poll(cls, context):
        return (context.mode == "OBJECT") and ( len(context.selected_objects) > 0 )

    def draw(self, context):
        lay = self.layout.column(align=True)

        row = lay.row(align=True)
        row.prop(self, 'unparentMethod', expand=True)

        lay.separator()

        row = lay.row(align=True)
        row.prop(self, 'unparentType', expand=True)

        lay.separator()

        row = lay.row(align=True)
        row.prop(self, 'delOrphanEmptyParents', expand=True)

    # END draw()

    def execute(self, context):

        if context.mode == "OBJECT":

            #ensure one of the selected objects is an active object
            if context.view_layer.objects.active is None:
                if len(context.selected_objects) > 0:
                    context.view_layer.objects.active = context.selected_objects[0]
            
            scn = context.scene
            
            activeObjName = context.view_layer.objects.active.name
            
            selObjNames = [] #declare
            for obj in context.selected_objects:
                objName = obj.name

                #find parent
                if obj.parent is not None:
                    parentName = obj.parent.name
                else:
                    parentName = ''

                #find grand parent
                if parentName != '':
                    parentObj = bpy.data.objects[parentName]

                    if parentObj.parent is not None:
                        grandParentName = parentObj.parent.name
                    else:
                        grandParentName = ''
                else:
                    grandParentName = ''


                selObjNames.append({'objName' : objName, 'parentName' : parentName, 'grandParentName' : grandParentName})

            
            for d in selObjNames:

                obj = bpy.data.objects[ d['objName'] ]

                if self.unparentType == "KEEPTFORM":
                    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

                elif self.unparentType == "UNPARENT":
                    bpy.ops.object.parent_clear(type='CLEAR')

                elif self.unparentType == "CLEAR_INVERSE":
                    bpy.ops.object.parent_clear(type='CLEAR_INVERSE')

            if self.unparentMethod == "ONELEVEL":

                for d in selObjNames:
                    obj = bpy.data.objects[ d['objName'] ]

                    #parent selected objects to their grandparent
                    if d['grandParentName'] != '':
                        grandParentObj = bpy.data.objects[ d['grandParentName'] ]

                        obj.parent = grandParentObj
                        obj.matrix_parent_inverse = grandParentObj.matrix_world.inverted()

            if self.delOrphanEmptyParents:

                emptiesToBeDeleted = set() #declare
                for d in selObjNames:    
                    #find empties that can be deleted
                    
                    if d['parentName'] != '':
                        
                        parentObj = bpy.data.objects[ d['parentName'] ]
                        
                        if parentObj.type == "EMPTY":

                            parentObjChildren = [ob_child for ob_child in bpy.context.scene.objects if ob_child.parent == parentObj]

                            #add empty to a list of empties to be deleted
                            if parentObjChildren == []:
                                emptiesToBeDeleted.add(parentObj)
                
                for empty in emptiesToBeDeleted:
                    bpy.data.objects.remove(empty, do_unlink=True)

                if self.unparentMethod == "CLEAR":
                    self.report({'INFO'}, 'Note: Not all empties may have been deleted when using "Clear to Root".  This is a limitation until a better method of deleting orphaned empties is implemented.' )


        else:
            self.report({'INFO'}, 'Unsupported mode detected.  Please use "Object Mode".' )
        

        return {'FINISHED'}
    # END execute()
# END Operator()
