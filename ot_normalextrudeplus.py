#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Name        : Normal Extrude+
# Description : An alternate (in some situations, more accurate) version of normal face extrusion
# Author      : Neltulz (Neil V. Moore)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import bpy
import bmesh
from .              import misc_functions
from .              import lay_misc

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

class NTZBNSUTLS_OT_normalextrudeplus(Operator):
    bl_idname = "ntzbnsutls.normalextrudeplus"
    bl_label = "Neltulz - Bonus Utils : Normal Extrude+"
    bl_description = 'An alternate (in some situations, more accurate) version of face normal extrusion.  Use this to replace Blender\'s "Extrude Along Normals"'
    bl_options = {'REGISTER', 'UNDO',
    #'PRESET'
    }

    objectModeAtBegin : StringProperty ()

    offsetAmount : FloatProperty (
        name="Offset Amount",
        description='Amount to offset faces by',
        default=0,
        soft_min=-10,
        soft_max=10,
    )

    showDissolveEdgesSection : BoolProperty (
        name="Show Dissolve Edges Section",
        default = False,
    )

    dissolveEdges : BoolProperty (
        name="Dissolve Edges",
        description="Dissolve Edges after offsetting faces",
        default = False,
    )

    dissolveUseVerts : BoolProperty (
        name="Dissolve Verts",
        description="Dissolve Verts when dissolving edges",
        default = True,
    )

    dissolveUseFaceSplit : BoolProperty (
        name="Face Split",
        description="Use Face Split when dissolving edges",
        default = False,
    )

    

    @classmethod
    def poll(cls, context):

        try:
            #try to determine objectMode
            objectModeAtBegin = bpy.context.object.mode
        except:
            objectModeAtBegin = "OBJECT"

        if objectModeAtBegin == "EDIT":

            activeObj = context.view_layer.objects.active
            if activeObj is not None:
                if activeObj.type == "MESH":
                    return True

    def execute(self, context):
        
        activeObjAtBegin = bpy.context.view_layer.objects.active

        if activeObjAtBegin is not None:

            offsetAmount = self.offsetAmount * -1

            if self.objectModeAtBegin == "EDIT":
                
                #store mesh data of active object in var
                me = activeObjAtBegin.data

                #create bmesh from mesh data of active object
                bm = bmesh.from_edit_mesh(me)
                
                #store list of selected faces & edges from the bmesh
                selFaces = {f for f in bm.faces if f.select}
                
                #Run solidify operator to offset faces
                bpy.ops.mesh.solidify(thickness=offsetAmount)

                #update bmesh after running the solidify operator
                bm = bmesh.from_edit_mesh(activeObjAtBegin.data)

                #store list of newly created faces
                selFacesAfterSolidify = {f for f in bm.faces if f.select}
                

                #delete the original selected faces because they are now leftover interior faces that are no longer useful
                bmesh.ops.delete(bm, geom=list(selFaces), context="FACES") #source: http://bit.ly/2uBIxqQ

                #store a list of linked faces (bmesh method that is similar to "grow selection")
                linkedFaces = {e.link_faces[0] for f in selFacesAfterSolidify for e in f.edges}

                #select the linked faces
                for f in linkedFaces:
                    f.select = True

                #update bmesh after growing selection
                bm = bmesh.from_edit_mesh(activeObjAtBegin.data)

                #update list of selected faces & edges from the bmesh
                allFaces = {f for f in bm.faces}
                selFacesAfterGrowing = {f for f in bm.faces if f.select}
                selEdges = {e for e in bm.edges if e.select}

                for f in selFacesAfterGrowing:
                    f.normal_flip()
                
                if self.dissolveEdges:
                    
                    for f in allFaces:
                        f.select = f not in selFacesAfterGrowing #invert selection

                    selEdgesInvert = {e for e in bm.edges if e.select}

                    
                    for f in allFaces:
                        f.select = False #deselect all faces

                    edgesToDissolve = {e for e in selEdges if e in selEdgesInvert}

                    bmesh.ops.dissolve_edges(bm, edges=list(edgesToDissolve), use_verts=self.dissolveUseVerts, use_face_split=self.dissolveUseFaceSplit)

                    #update allFaces
                    allFaces = {f for f in bm.faces}
                    
                    for f in selFacesAfterGrowing & allFaces:
                        f.select = True #select faces after growing

                        '''
                        if f in allFaces: #safety check to ensure face exists
                            f.select = True
                        '''
                        

                else:
                    
                    #select faces after solidify, but before growing selection (deselects the walls) (similar to select less)
                    for f in allFaces:
                        f.select = f in selFacesAfterSolidify

                #write bmesh back to the active object's mesh data to show the changes
                bmesh.update_edit_mesh(me, True)

        return {'FINISHED'}

    
    def draw(self, context):
 
        if self.objectModeAtBegin == "EDIT":

            scn = context.scene
            layout = self.layout.column(align=True)
            
            offsetAmountRow = layout.row(align=True)
            offsetAmountRow.prop(self, "offsetAmount", slider=True)
            offsetAmountRow.separator()

            layout.separator()

            if self.showDissolveEdgesSection:
                dissolveEdgesWrapper = layout.box().column(align=True)
            else:
                dissolveEdgesWrapper = layout

            lay_misc.createShowHide(self, context, None, None, "showDissolveEdgesSection", "dissolveEdges", "Dissolve Edges", dissolveEdgesWrapper)

            if self.showDissolveEdgesSection:

                dissolveEdgesWrapper.separator()

                row = dissolveEdgesWrapper.row(align=True)
                spacer = row.label(text="", icon="BLANK1")

                colInner = row.column(align=True)

                dissolveOptions = colInner.row(align=False)
                row = dissolveOptions.row(align=True)
                row.prop(self, "dissolveUseVerts", toggle=True)

                row = dissolveOptions.row(align=True)
                row.prop(self, "dissolveUseFaceSplit", toggle=True)

    #END draw()
    

    def invoke(self, context, event):

        try:
            #try to determine objectMode
            objectModeAtBegin = bpy.context.object.mode
        except:
            objectModeAtBegin = "OBJECT"
        
        self.objectModeAtBegin = objectModeAtBegin
        
        if objectModeAtBegin == "EDIT":
            return self.execute(context)
        
        else:
            return {'FINISHED'}
    #END invoke()

#END Operator()