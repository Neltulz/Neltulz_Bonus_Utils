#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Name        : Offset All Faces
# Description : Offset All Faces using a solidify modifier
# Author      : Neltulz (Neil V. Moore)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import bpy
import bmesh
from .              import misc_functions
from .              import lay_misc

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

class NTZBNSUTLS_OT_offsetfaces(Operator):
    bl_idname = "ntzbnsutls.offsetfaces"
    bl_label = "Neltulz - Bonus Utils : Offset All Faces"
    bl_description = "Offset All Faces using a solidify modifier"
    bl_options = {'REGISTER', 'UNDO',
    #'PRESET'
    }

    objectModeAtBegin : StringProperty () #determined in invoke()

    keepModifier : BoolProperty(
        name="Keep Modifier",
        description='Does not apply the solidify modifier when finished so that the user may continue to modify its settings',
        default = False
    )

    offsetAmount : FloatProperty (
        name="Offset Amount",
        description='Amount to offset faces by',
        default=0,
        soft_min=-10,
        soft_max=10,
    )

    

    @classmethod
    def poll(cls, context):
        activeObj = context.view_layer.objects.active

        if activeObj is not None:
            if activeObj.type == "MESH":
                return True

    def execute(self, context):
        
        activeObjAtBegin = bpy.context.view_layer.objects.active

        if activeObjAtBegin is not None:
            
            if activeObjAtBegin.type == "MESH":
                
                offsetAmount = self.offsetAmount * -1

                if self.objectModeAtBegin in ["OBJECT", "EDIT"]:

                    if self.objectModeAtBegin == "EDIT":
                        bpy.ops.object.mode_set(mode='OBJECT')

                    neltulzOffsetModifier = misc_functions.findModifier(self, context, activeObjAtBegin, "Neltulz - Offset Faces") #declare


                    if neltulzOffsetModifier is None:
                        activeObjAtBegin.modifiers.new(name="Neltulz - Offset Faces", type='SOLIDIFY')

                        neltulzOffsetModifier = misc_functions.findModifier(self, context, activeObjAtBegin, "Neltulz - Offset Faces")
                    
                    if self.offsetAmount > 0:
                        use_flip_normals = False
                    else:
                        use_flip_normals = True

                    

                    neltulzOffsetModifier.show_on_cage = True
                    neltulzOffsetModifier.thickness = offsetAmount
                    neltulzOffsetModifier.use_flip_normals = use_flip_normals
                    neltulzOffsetModifier.use_even_offset = True
                    neltulzOffsetModifier.use_quality_normals = True
                    neltulzOffsetModifier.use_rim = True
                    neltulzOffsetModifier.use_rim_only = True

                    if not self.keepModifier:
                        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Neltulz - Offset Faces")

                    bpy.ops.object.mode_set(mode=self.objectModeAtBegin) #switch back to mode at begin
                
        return {'FINISHED'}

    
    def draw(self, context):
        scn = context.scene
        layout = self.layout.column(align=True)
        
        offsetAmountRow = layout.row(align=True)
        offsetAmountRow.prop(self, "offsetAmount", slider=True)
        offsetAmountRow.separator()

        layout.separator()

        row = layout.row(align=True)
        row.prop(self, "keepModifier")

    #END draw()
    

    def invoke(self, context, event):

        try:
            #try to determine objectMode
            objectModeAtBegin = bpy.context.object.mode
        except:
            objectModeAtBegin = "OBJECT"
        
        self.objectModeAtBegin = objectModeAtBegin

        return self.execute(context)
    #END invoke()

#END Operator()






