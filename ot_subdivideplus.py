#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Name        : Subdivide+
# Description : Subdivide+ and then select the newly created edges
# Author      : iceythe (Kaio)
# Permission  : Special thanks to iceythe for the creation of this script and permission to include it with the Neltulz - Bonus Utils add-on
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import bpy
import bmesh

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

class NTZBNSUTLS_OT_subdivideplus(Operator):
    bl_idname = 'ntzbnsutls.subdivideplus'
    bl_description = 'Subdivide with additional features for automatically selecting newly added vertices and edgse, etc.'
    bl_label = 'Subdivide+'
    bl_options = {'REGISTER', 'UNDO'}

    _falloffs = (('SMOOTH', 'Smooth', '', 0),
                 ('SPHERE', 'Sphere', '', 1),
                 ('ROOT', 'Root', '', 2),
                 ('SHARP', 'Sharp', '', 3),
                 ('LINEAR', 'Linear', '', 4),
                 ('INVERSE_SQUARE', 'Inverse Square', '', 5))

    _corner_type = (('STRAIGHT_CUT', 'Straight Cut', '', 0),
                    ('INNER_VERT', 'Inner Vert', '', 1),
                    ('PATH', 'Path', '', 2),
                    ('FAN', 'Fan', '', 3))

    _single_edge = None
    flatten: BoolProperty(name='Flatten', default=True)
    _flat_swap = False
    _smooth_val = 0.0

    cuts: IntProperty(name='Number Cuts', default=1,
                      min=1, max=500)
    smooth: FloatProperty(name='Smoothness', default=0.0, min=-2.0)
    falloff: EnumProperty(name='Smooth Falloff', default='SMOOTH',
                          items=_falloffs)
    quad_corner: EnumProperty(name='Quad Corner Type',
                              default='INNER_VERT', items=_corner_type)

    grid_fill: BoolProperty(name='Grid Fill', default=True)
    single_edge: BoolProperty(name='Single Edge', default=False)
    only_quads: BoolProperty(name='Only Quads', default=False)
    sphere: BoolProperty(name='Spherize', default=False)
    smooth_even: BoolProperty(name='Even Smoothing', default=False)

    fractal: FloatProperty(name='Fractal Noise', default=0.0)
    along_normal: FloatProperty(name='Along Normal', default=0.0)
    seed: IntProperty(name='Seed', default=0)
    edge_percents: FloatProperty(name='Edge Percent', default=0.5,
                                 min=0.0, max=1.0)

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH' and
                context.object.data.total_edge_sel)

    def is_individual(self, edges):
        for edge in edges:
            for v in edge.verts:
                for e in v.link_edges:
                    if e.select and e is not edge:
                        return False
        return True

    def execute(self, context):
        smooth_val = self._smooth_val
        flat_swap = self._flat_swap
        smooth = self.smooth
        flatten = self.flatten
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        totface = me.total_face_sel

        msm = context.tool_settings.path_resolve('mesh_select_mode', False)

        edges_pre = set(bm.edges)
        edges = [e for e in bm.edges if e.select]
        individual = self.is_individual(edges)

        if smooth != 0 and flatten and not flat_swap:
            self.flatten = flatten = False
            self._flat_swap = flat_swap = True

        if smooth != 0 and flatten and flat_swap:
            self._smooth_val = smooth_val = smooth
            self.smooth = smooth = 0
            self._flat_swap = flat_swap = False

        elif smooth == 0 and not flatten and smooth_val is not None:
            self.smooth = smooth_val
            self._smooth_val = None
            self._flat_swap = True

        edge_percents = {}
        if self.edge_percents != 0.5:
            edge_percents = {e: self.edge_percents for e in edges}

        ret = bmesh.ops.subdivide_edges(
            bm, edges=edges, use_smooth_even=self.smooth_even,
            smooth_falloff=self.falloff, fractal=self.fractal,
            along_normal=self.along_normal, use_sphere=self.sphere,
            quad_corner_type=self.quad_corner, seed=self.seed,
            use_single_edge=self.single_edge, cuts=self.cuts,
            use_only_quads=self.only_quads, smooth=self.smooth,
            edge_percents=edge_percents, use_grid_fill=self.grid_fill)

        geom_inner = ret['geom_inner']
        inner = ret['geom_inner']
        split = ret['geom_split']

        if individual and len(edges) > 1:
            # assume vert select mode
            for elem in ret['geom']:
                elem.select = False
                bm.select_history.add(geom_inner[-1])
                geom_inner[-1].select = True

            for elem in geom_inner:
                elem.select = True

        elif msm[:] == (1, 0, 0):
            for v in bm.verts:
                v.select = False
            for elem in ret['geom']:
                if isinstance(elem, bmesh.types.BMVert):
                    elem.select = True

        elif (len(edges) == 1 and len(geom_inner) == 1) or self._single_edge:
            bm.select_mode = {'VERT'}
            vert = geom_inner[0]
            bm.select_history.add(vert)
            msm[:] = 1, 0, 0
            self._single_edge = True
            for elem in geom_inner:
                elem.select = True


        elif msm[:] == (0, 1, 0) and not totface:
            # print("edges mode, quad corner")
            for elem in ret['geom']:
                elem.select = False

            edges_post = set(bm.edges).difference(edges_pre)
            geom = set(j for i in ret.values() for j in i)
            corner_geom = [e for e in edges_post if e not in geom]
            for e in corner_geom:
                if any([True for v in e.verts if v in split]):
                    e.select = True
                    continue
                e.select = False

            for e in inner:
                if isinstance(e, bmesh.types.BMEdge):
                    e.select = True

        else:
            for elem in geom_inner:
                elem.select = True
        bm.select_flush_mode()
        bmesh.update_edit_mesh(me)
        return {'FINISHED'}
