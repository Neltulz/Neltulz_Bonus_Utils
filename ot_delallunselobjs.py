#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Name        : Del all Unsel Objs
# Description : Delete all Unselected Objects
# Author      : Neltulz (Neil V. Moore)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import bpy
from . import misc_functions

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Operator)


class NTZBNSUTLS_OT_delallunselobjs(Operator):
    """Tooltip"""
    bl_idname = "ntzbnsutls.delallunselobjs"
    bl_label = "Neltulz - Bonus Utils : Delete all Unsel Objs"
    bl_description = "Deletes all unselected objects including their collections"
    bl_options = {'REGISTER', 'UNDO'}

    delOrphanedColls : BoolProperty(
        name        = "Delete Orphaned Collections",
        default     = True
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

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
        
        return {'FINISHED'}
        
        
    # END execute()

# END Operator()