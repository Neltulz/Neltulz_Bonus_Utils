#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Name        : Sel Contig Edges
# Description : Select Contiguous Edges - Grow Edge Selection By Angle
# Author      : iceythe (Kaio)
# Permission  : Special thanks to iceythe for the creation of this script and permission to include it with the Neltulz - Bonus Utils add-on
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import bpy
import bmesh
from math import degrees
from math import radians
from operator import itemgetter
from . import miscFunc

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)


def edges_indiv_get(bm, maxAngle):
    walked = set()
    links = []
    rec_count = 0

    def links_get(e):
        def get_next(e, v_prev=None):
            nonlocal rec_count
            if rec_count > 900:
                return
            for v in e.verts:
                for e2 in v.link_edges:
                    if e2.select:
                        v1 = e2.other_vert(v).co - v.co
                        v2 = e.other_vert(v).co - v.co
                        deg = degrees(v1.angle(v2))
                        if deg > 90:
                            deg -= (deg - 90)
                        if 0 < deg > maxAngle:
                            indiv.add(e2)
                        if e2 not in walked:
                            walked.add(e)
                            chain.append(e2)
                            rec_count += 1
                            get_next(e2)

        walked.add(e)
        chain = []
        get_next(e)
        links.append(chain)

    indiv = set()
    for e in [e for e in bm.edges if e.select]:
        if e not in walked:
            indiv.add(e)
            links_get(e)
    return indiv


class VIEW3D_OT_ntzbu_select_contiguous_edges(Operator):
    bl_idname           = "view3d.ntzbu_select_contiguous_edges"
    bl_label            = "NTZBU : Select Contiguous Edges"
    bl_description      = "Select Contiguous Edges - Grow Edge Selection By Angle"
    bl_options          = {'REGISTER', 'UNDO', 'PRESET'}

    
    bUseOverridesFromAddonPrefs : BoolProperty(
        name="Use Overrides from Add-on Preferences",
        description='Gets operator properties from the addon-preferences.  This will override any settings in the user customized keymap.  If you want to prevent the addon preferences from setting your operator properties, set this to False',
        default = True
    )
    

    reset_maxAngle : BoolProperty( name = "Reset Max Angle", default = False )
    maxAngle : IntProperty(
        name        = "Max Angle",
        default     = 15,
        min         = 0,
        max         = 180,
    )

    
    reset_maxEdges : BoolProperty( name = "Reset Max Edges", default = False )
    maxEdges : IntProperty(
        name        = "Max Edges",
        default     = 0,
        min         = 0,
        soft_max    = 50
    )

    direction_List = (
        ('BACKWARD', "Backward", "", "", 0),
        ('BOTH',     "Both",     "", "", 1),
        ('FORWARD',  "Forward",  "", "", 2),
    )

    reset_direction : BoolProperty( name = "Reset Direction", default = False )
    direction : EnumProperty(
        items			= direction_List,
        name			= "Direction",
        description		= "Search Direction",
        default			= 'BOTH',
    )

    reset_direction : BoolProperty(
        name        = "Reset Direction",
        default     = False
    )

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH' and
                getattr(context.object.data, "total_edge_sel", 0))


    def invoke(self, context, event):
        scn = context.scene

        addonPrefs = context.preferences.addons[__package__].preferences

        # BEGIN Retreive Operator properties from addon preferences
        opPropNameList = ['maxAngle', 'maxEdges', 'direction']
        miscFunc.retreive_op_props_from_addonPrefs(self, context, addonPrefs=addonPrefs, opPropNameList=opPropNameList, opPropPrefix='selContigEdg_')
        # END Retreive Operator properties from addon preferences

        return self.execute(context)
    #END invoke()

    def execute(self, context):
        self.contiguous_edge(context)
        return {'FINISHED'}
    #END execute()

    def draw(self, context):
        scn = context.scene
        layout = self.layout.column(align=True)

        layout.separator()

        maxAngleRow = layout.row(align=True)
        maxAngleRow.prop(self, "maxAngle", slider=True)
        maxAngleRow.separator()
        resetBtn = maxAngleRow.row(align=True)
        resetBtn.active = False
        resetBtn.prop(self, "reset_maxAngle", toggle=True, text="", icon="LOOP_BACK", emboss=False)

        maxEdgesRow = layout.row(align=True)
        maxEdgesRow.prop(self, "maxEdges", slider=True)
        maxEdgesRow.separator()
        resetBtn = maxEdgesRow.row(align=True)
        resetBtn.active = False
        resetBtn.prop(self, "reset_maxEdges", toggle=True, text="", icon="LOOP_BACK", emboss=False)

        layout.separator()

        directionRow = layout.row(align=True)
        directionRow.prop(self, "direction", expand=True)
        directionRow.separator()
        resetBtn = directionRow.row(align=True)
        resetBtn.active = False
        resetBtn.prop(self, "reset_direction", toggle=True, text="", icon="LOOP_BACK", emboss=False)
    #END draw()

    def contiguous_edge(self, context):

        propsToReset = [
            ["reset_maxAngle", ["maxAngle"] ],
            ["reset_maxEdges", ["maxEdges"] ],
            ["reset_direction", ["direction"] ],
        ]

        miscFunc.resetOperatorProps(self, context, propsToReset)
        
        ob = bpy.context.object
        bm = bmesh.from_edit_mesh(ob.data)
        max_rad = radians(self.maxAngle)

        for e in edges_indiv_get(bm, self.maxAngle):

            pool = [e]
            walked = set(pool)
            _pool = pool.copy()
            _walked = walked.copy()

            # Find the next straight edge
            def get_next(links, a, angle, aco):
                rads = [(angle(e.other_vert(a).co - aco), e) for e in links]
                if rads:
                    angle, edge = sorted(rads, key=itemgetter(0))[0]
                    if angle <= max_rad:
                        return edge

            if self.direction == 'BOTH':
                verts = pool[0].verts
            elif self.direction == 'FORWARD':
                verts = pool[0].verts[0],
            else:
                verts = pool[0].verts[1],

            for v in verts:
                iterations = 0
                update = walked.update
                append = pool.append
                pop = pool.pop
                while pool and (not self.maxEdges or (iterations < self.maxEdges)):
                    e = pop()
                    links = [e for e in v.link_edges if e not in walked]
                    update(links)
                    vco = v.co
                    edge = get_next(links, v, (v.co - e.other_vert(v).co).angle, vco)
                    if edge:
                        v = edge.other_vert(v)
                        edge.select_set(True)
                        append(edge)
                        iterations += 1
                walked = _walked
                pool = _pool

        bmesh.update_edit_mesh(ob.data)
    # END contiguous_edge()


#END Operator()