import bpy
import bmesh
from operator import itemgetter
from mathutils import Vector

import numpy
from itertools import chain
from itertools import permutations


def average(lst): 
    return sum(lst) / len(lst) 

def meanVector(lst):

    xLst = [x for x in lst[0]]
    #yLst = [y for y in lst[1]]
    #zLst = [z for z in lst[2]]

    #vectorList = xLst + yLst + zLst

    #result = (numpy.mean(xLst), numpy.mean(yLst), numpy.mean(zLst) )
    #result = numpy.mean(vectorList)

    arr = numpy.array(lst).reshape(len(lst), 3)
    result = numpy.mean(arr, axis=0)
    
    return result

def middleVector(lst):

    xLst = [x[0] for x in lst]
    yLst = [y[1] for y in lst]
    zLst = [z[2] for z in lst]

    xMinMax = [min(xLst), max(xLst)]
    yMinMax = [min(yLst), max(yLst)]
    zMinMax = [min(zLst), max(zLst)]

    result = ( average( xMinMax ), average( yMinMax ), average( zMinMax ) )

    return result


# -----------------------------------------------------------------------------
#   Determine which mode is currently Selected (Vert, Edge, Face, etc)
#   Returned: (0=Multiple modes, 1=Vertice Mode, 2=Edge Mode, 3=Face Mode)
# -----------------------------------------------------------------------------

def getCurrentSelectMode(self, context):
    #Create empty list
    tempList = []

    #check current mesh select mode
    for bool in bpy.context.tool_settings.mesh_select_mode:
        tempList.append(bool)
    
    #convert list into a tuple
    tempTuple = tuple(tempList)

    currentSelectMode = int()

    
    if tempTuple == (True, False, False):       
        currentSelectMode = 1
    elif tempTuple == (False, True, False):
        currentSelectMode = 2
    elif tempTuple == (False, False, True):
        currentSelectMode = 3
    else:
        pass #(defaults currentSelectMode to 0)

    return currentSelectMode
# END getCurrentSelectMode(self, context)



#Reset Operators to their default values:
def resetOperatorProps(self, context, propsToReset):

    # EXAMPLE OF propsToReset - ADD THIS TO THE TOP OF THE execute() IN YOUR OPERATOR AND CUSTOMIZE
    #
    # propsToReset = [
    #     ["reset_allVisibilityModes", ["render", "realtime", "editmode", "cage"] ],
    #     ["reset_affect", ["affect"] ],
    # ]

    for item in propsToReset:

        resetBoolPropName = item[0]
        resetBool = getattr(self, resetBoolPropName)

        if resetBool == True:

            for propName in item[1]:
                defaultVal = self.__annotations__[propName][1]['default']

                setattr(self, propName, defaultVal)
                setattr(self, resetBoolPropName, False)

def getSelObjs(self, context):
    return bpy.context.selected_objects

def getScnObjs(self, context):
    return context.scene.objects

def getUnselObjs(self, context):
    allObjs = context.scene.objects
    selObjs = context.selected_objects
    return [obj for obj in allObjs if obj not in selObjs] #unselected objs

def findModifier(self, context, obj, modifierName):

    foundModifier = None #declare
    for modifier in obj.modifiers:
    
        if modifier.name == modifierName:
            foundModifier = modifier
            break

    return foundModifier

def findVertexGroup(self, context, obj, vertexGroupName):

    foundVG = None #declare
    for vg in obj.vertex_groups:
    
        if vg.name == vertexGroupName:
            foundVG = vg
            break

    return foundVG


def bboxFromSelection():

    #returns the bounding box of a selection.  Special thanks and Source: iceythe
    all_vcos = []
    # Get all vert cos from objects in edit mode
    for o in bpy.context.objects_in_mode_unique_data:
        bm = bmesh.from_edit_mesh(o.data)
        mat = o.matrix_world
        all_vcos.extend([mat @ v.co for v in bm.verts if v.select])

    (x1, y1, z1,
     x2, y2, z2) = [func(all_vcos, key=itemgetter(i))[i]
                    for func in (min, max) for i in range(3)]

    bbox = (
        (x1, y1, z1), (x1, y1, z2),
        (x2, y1, z2), (x2, y1, z1),

        # mirror other size
        (x1, y2, z1), (x1, y2, z2),
        (x2, y2, z2), (x2, y2, z1))

    bbox_vecs = [Vector(i) for i in bbox]

    return bbox_vecs

def dimensionsFromSelection(self, context, minMaxAvg='AVG'):

    #Get dimension from selection - Special thanks & source: iceythe

    all_vcos = []
    # Get all vert cos from objects in edit mode
    for o in bpy.context.objects_in_mode_unique_data:
        bm = bmesh.from_edit_mesh(o.data)
        mat = o.matrix_world
        all_vcos.extend([(mat @ v.co)[:] for v in bm.verts if v.select])

    it = numpy.fromiter(chain.from_iterable(all_vcos), dtype=float)
    it.shape = (len(all_vcos), 3)
    _min, _max = Vector(it.min(0).tolist()), Vector(it.max(0).tolist())

    if minMaxAvg == "MIN":
        result = min((_max - _min))
    elif minMaxAvg == "MAX": 
        result = max((_max - _min))
    elif minMaxAvg == "AVG":
        result = average((_max - _min))

    return result

def activateProp(self, context, propName=''):

    addonPrefs = bpy.context.preferences.addons[__package__].preferences

    if not addonPrefs.preventInfiniteRecursion:

        addonPrefs.preventInfiniteRecursion = True

        prop        = getattr(addonPrefs, propName, None)
        prop_active = getattr(addonPrefs, f'{propName}_active', None)

        if prop_active is not None:

            setattr(addonPrefs, f'{propName}_active', True)

        addonPrefs.preventInfiniteRecursion = False

def deactivateProp(self, context, propName=''):
    addonPrefs = bpy.context.preferences.addons[__package__].preferences

    if not addonPrefs.preventInfiniteRecursion:

        addonPrefs.preventInfiniteRecursion = True

        prop        = getattr(addonPrefs, propName, None)
        defaultVal  = self.__annotations__[propName][1]['default']

        if prop is not None:

            setattr(addonPrefs, propName, defaultVal)

        addonPrefs.preventInfiniteRecursion = False

def retreive_op_props_from_addonPrefs(self, context, addonPrefs=None, opPropNameList=None, opPropPrefix=None):

    if self.bUseOverridesFromAddonPrefs:

        for opPropName in opPropNameList:
            
            #get the value of the addonPrefs property
            addonPropActive = getattr(addonPrefs, f'{opPropPrefix}{opPropName}_active', None)

            if addonPropActive is not None:
                
                if addonPropActive:

                    addonPropVal = getattr(addonPrefs, f'{opPropPrefix}{opPropName}', None)

                    #set the value of the operator property to the value of the addonPrefs property
                    setattr(self, opPropName, addonPropVal)

# END retreive_op_props_from_addonPrefs()

def getOutliners(self, context):
    outliners = [] #declare
    for win in context.window_manager.windows:
        for area in win.screen.areas:
            if area.type == 'OUTLINER':
                outliners.append({'window' : win, 'area': area})

    return outliners

# END getOutliners()

def expand_selected_objs_in_outliner(self, context, selObjs=None, outliners=None, activeObj=None):

    if activeObj is None:
        activeObj = context.view_layer.objects.active

    if selObjs is None:
        selObjs = context.selected_objects

    if outliners is None:
        outliners = getOutliners(self, context)

    for obj in selObjs:
        
        context.view_layer.objects.active = obj #set object as active object

        for outliner in outliners:
            win = outliner['window']
            area = outliner['area']

            contextOverride = {'window': win, 'screen': win.screen, 'area': area}
            bpy.ops.outliner.show_active(contextOverride)

    if activeObj is not None:
        context.view_layer.objects.active = activeObj #reset Active Object

        
# END expand_selected_objs_in_outliner()

def redraw_all_outliners(self, context, outliners=None):

    if outliners is None:
        outliners = getOutliners(self, context)

    for outliner in outliners:
        outliner['area'].tag_redraw() #redraw outliner

# END redraw_all_outliners()


def snapCursorToMedianPoint(self, context, activeObj=None, objMode=None, tformPivotPoint=None):

    if activeObj is None:
        activeObj = context.view_layer.objects.active

    if objMode is None:
        objMode is context.object.mode

    if tformPivotPoint is None:
        tformPivotPoint = f'{context.scene.tool_settings.transform_pivot_point}'

    if activeObj.type == "MESH":
        

        if objMode == "OBJECT":
            
            
            if tformPivotPoint == "ACTIVE_ELEMENT":
                bpy.ops.view3d.snap_cursor_to_active()

            elif tformPivotPoint == "INDIVIDUAL_ORIGINS":
                context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
                bpy.ops.view3d.snap_cursor_to_selected()
                context.scene.tool_settings.transform_pivot_point = tformPivotPoint #reset
                

            else:
                bpy.ops.view3d.snap_cursor_to_selected()
        else:
            bpy.ops.view3d.snap_cursor_to_selected()

    else:
        if tformPivotPoint == "ACTIVE_ELEMENT":
            bpy.ops.view3d.snap_cursor_to_active()

        else:
            bpy.ops.view3d.snap_cursor_to_selected()
# END snapCursorToMedianPoint()

def snapCursorToBoundingBoxCenter(self, context, activeObj=None, objMode=None, tformPivotPoint=None, numObjsWithVertsSel=None):

    if activeObj is None:
        activeObj = context.view_layer.objects.active

    if objMode is None:
        objMode = context.object.mode

    if tformPivotPoint is None:
        tformPivotPoint = f'{context.scene.tool_settings.transform_pivot_point}'

    if activeObj.type == "MESH":

        if objMode == "OBJECT":
            
            if tformPivotPoint == "ACTIVE_ELEMENT":
                bpy.ops.view3d.snap_cursor_to_active()

            else:
                bpy.ops.view3d.snap_cursor_to_selected()

        else:

            if numObjsWithVertsSel is not None:

                if numObjsWithVertsSel == 1:  

                    bm = bmesh.from_edit_mesh(activeObj.data)
                    mat = activeObj.matrix_world.copy()

                    vco = [v.co for v in bm.verts if v.select]
                    arr = np.array(vco).reshape(len(vco), 3)

                    center = mat @ Vector((arr.min(axis=0) + arr.max(axis=0)) * 0.5)

                    context.scene.cursor.location = center
                
                if numObjsWithVertsSel >= 2:
                    bpy.ops.view3d.snap_cursor_to_selected() #sloppy fallback
    
    else:
        if tformPivotPoint == "ACTIVE_ELEMENT":
            bpy.ops.view3d.snap_cursor_to_active()

        else:
            bpy.ops.view3d.snap_cursor_to_selected()
# END snapCursorToBoundingBoxCenter()


def max_dim_from_objs_or_empties(self, context, minMaxAvg='AVG', objs=None):

    #Get max dimension from objects and empties - Special thanks & source: iceythe
    all_vcos = []
    for o in objs:
        mat_w = o.matrix_world
        if o.type == 'EMPTY':
            size = o.empty_display_size
            all_vcos.extend([mat_w @ Vector(point) for point in
                            permutations((-size, size) * 2, 3)])
            continue
        all_vcos.extend([mat_w @ Vector(point[:])
                        for point in o.bound_box[:]])

    it = numpy.fromiter(chain.from_iterable((all_vcos)), dtype=float)
    it.shape = (len(all_vcos), 3)
    _min, _max = Vector(it.min(0).tolist()), Vector(it.max(0).tolist())

    if minMaxAvg == "MIN":
        result = min((_max - _min))
    elif minMaxAvg == "MAX": 
        result = max((_max - _min))
    elif minMaxAvg == "AVG":
        result = average((_max - _min))

    #prevent zero result
    if result == 0:
        result = 1

    return result
# END max_dim_from_objs_or_empties()