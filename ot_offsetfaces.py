#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Name        : Offset Faces
# Description : Offset Faces using a solidify modifier
# Author      : Neltulz (Neil V. Moore)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import bpy
import bmesh
from . import misc_functions

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

class NTZBNSUTLS_OT_offsetfaces(Operator):
    bl_idname = "ntzbnsutls.offsetfaces"
    bl_label = "Neltulz - Bonus Utils : Offset Faces"
    bl_description = "Offset Faces"
    bl_options = {'REGISTER', 'UNDO',
    #'PRESET'
    }

    
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
        
        if bpy.context.view_layer.objects.active is not None:
            return True

    def execute(self, context):
        
        activeObjAtBegin = bpy.context.view_layer.objects.active

        if activeObjAtBegin is not None:

            modeAtBegin = "Unknown"
            try:
                #try to determine objectMode
                modeAtBegin = bpy.context.object.mode
            except:
                modeAtBegin = "OBJECT"


            neltulzOffsetModifier = misc_functions.findModifier(self, context, activeObjAtBegin, "Neltulz - Offset Faces") #declare


            if neltulzOffsetModifier is None:
                activeObjAtBegin.modifiers.new(name="Neltulz - Offset Faces", type='SOLIDIFY')

                neltulzOffsetModifier = misc_functions.findModifier(self, context, activeObjAtBegin, "Neltulz - Offset Faces")

            

            if neltulzOffsetModifier is not None:
                if self.offsetAmount > 0:
                    use_flip_normals = False
                else:
                    use_flip_normals = True

                offsetAmount = self.offsetAmount * -1

                neltulzOffsetModifier.show_on_cage = True
                neltulzOffsetModifier.thickness = offsetAmount
                neltulzOffsetModifier.use_flip_normals = use_flip_normals
                neltulzOffsetModifier.use_even_offset = True
                neltulzOffsetModifier.use_quality_normals = True
                neltulzOffsetModifier.use_rim = True
                neltulzOffsetModifier.use_rim_only = True

                if not self.keepModifier:
                    if modeAtBegin == "EDIT":
                        bpy.ops.object.mode_set(mode='OBJECT')

                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Neltulz - Offset Faces")

                    if modeAtBegin == "EDIT":
                        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

    
    def draw(self, context):
        scn = context.scene
        layout = self.layout.column(align=True)
        
        offsetAmountRow = layout.row(align=True)
        offsetAmountRow.prop(self, "offsetAmount", slider=True)
        offsetAmountRow.separator()

        layout.separator()

        keepModifierRow = layout.row(align=True)
        keepModifierRow.prop(self, "keepModifier")

    #END draw()
    

    '''
    def invoke(self, context, event):
        scn = context.scene
        
        if self.bForcePanelOptions:

            if scn.ntzbnsutls_selcontigedg.useCustomSettings == "CUSTOM":
                
                #prop list
                propList = ['maxAngle', 'maxEdges', 'direction']

                for prop in propList:
                    
                    #get the value of the scene property
                    scnPropVal = getattr(scn.ntzbnsutls_selcontigedg, prop)

                    #set the value of the operator property to the value of the scene property
                    setattr(self, prop, scnPropVal)

        return self.execute(context)
    #END invoke()
    '''

#END Operator()