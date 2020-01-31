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

def dimensionsFromSelection(self, context, minMaxAvg):

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