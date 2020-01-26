import bpy
        

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