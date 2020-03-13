#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Name        : Del all Unsel Objs
# Description : Delete all Unselected Objects
# Author      : Neltulz (Neil V. Moore)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import ctypes
import bpy
from . import miscFunc

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Operator)

class VIEW3D_OT_ntzbu_delete_all_unselected_objs(Operator):
    """Tooltip"""
    bl_idname           = "view3d.ntzbu_delete_all_unselected_objs"
    bl_label            = "NTZBU : Delete all Unselected Objects"
    bl_description      = "Deletes all unselected objects including their collections"
    bl_options          = {'REGISTER', 'UNDO'}


    drawConfirmDiag = False

    delOrphanedColls : BoolProperty (
        name        = 'Delete Orphaned Collections',
        default     = True,
    )

    @classmethod
    def poll(cls, context):
        return True

    
    def invoke(self, context, event):

        addonPrefs = context.preferences.addons[__package__].preferences

        if addonPrefs.delUnselObjs_useConfirmDiag == "YES":
            self.drawConfirmDiag = True
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)
    # END invoke()

    def draw(self, context):
        lay = self.layout.column(align=True)

        if self.drawConfirmDiag:
            lay.label(text="Are you sure?")
        
        else:
            lay.prop(self, "delOrphanedColls")
    # END draw()

    def execute(self, context):

        self.drawConfirmDiag = False #reset

        scn = context.scene

        #store list of objects & selected objects
        objs = bpy.data.objects
        selObjs = bpy.context.selected_objects

        objs_to_be_removed = set() #declare

        #find objects that need to be removed and add them to to the objs_to_be_removed set
        for obj in objs:
            if obj not in selObjs:
                objs_to_be_removed.add(obj)
                    
        
        #remove all objects in the objs_to_be_removed set
        for obj in objs_to_be_removed:
            objs.remove(obj, do_unlink=True)

        if self.delOrphanedColls:

            #store list of objects & selected objects
            objs = bpy.data.objects
            selObjs = context.selected_objects


            for collection in bpy.data.collections:

                for obj in collection.all_objects:
                    
                    if obj in selObjs:
                        break

                else: #for loop did not break (no objects found in the list of selected objects)
                    bpy.data.collections.remove(collection)

        self.useConfirmDiag = True #reset
        
        return {'FINISHED'}
    # END execute()


# END Operator()