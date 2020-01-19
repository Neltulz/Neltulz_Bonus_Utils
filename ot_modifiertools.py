#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Name        : Change All Modifier Visibility
# Description : Delete all Unselected Objects
# Author      : Neltulz (Neil V. Moore)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import bpy
from . import misc_functions

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Operator)


class NTZBNSUTLS_OT_modifiervisibility(Operator):
    """Tooltip"""
    bl_idname = "ntzbnsutls.modifiervisibility"
    bl_label = "Neltulz - Bonus Utils : Modifier Visibility"
    bl_description = "Enables/Disables Modifiers"
    bl_options = {'REGISTER', 'UNDO'}

    tooltip : StringProperty(options={'HIDDEN'})

    bForcePanelOptions : BoolProperty(
        name="Force Panel Options",
        description='Gets all of the operator properties from the sidebar panel options.  This will override any settings in the user customized keymap.',
        default = False
    )

    enableDisableToggle_List = [
        ("ENABLE",  "Enable",   "Enable modifiers",  "", 0),
        ("TOGGLE",  "Toggle",   "Toggle modifiers",  "", 1),
        ("DISABLE", "Disable",  "Disable modifiers", "", 2),
    ]

    enableDisableToggle : EnumProperty (
        items       = enableDisableToggle_List,
        name        = "Settings",
        default     = "TOGGLE"
    )

    render : BoolProperty (
        name="Render",
        description="Change Render Visibility for modifiers",
        default = True,
    )

    realtime : BoolProperty (
        name="Realtime",
        description="Change Realtime Visibility for modifiers",
        default = True,
    )

    editmode : BoolProperty (
        name="Edit Mode",
        description="Change Edit Mode Visibility for modifiers",
        default = False,
    )

    cage : BoolProperty (
        name="Cage",
        description="Change Cage Visibility for modifiers",
        default = False,
    )

    affect_List = [
        ("SEL",       "Selected",   "", "", 0),
        ("ALL",       "All",        "", "", 1),
        ("UNSEL",     "Unselected", "", "", 2),
    ]

    reset_affect : BoolProperty( name = "Reset Affect", default = False )
    affect : EnumProperty (
        items       = affect_List,
        name        = "Affect",
        description = "Which objects to affect",
        default     = "SEL"
    )

    reset_allVisibilityModes : BoolProperty(
        name        = "Reset All Visibility Modes",
        default     = False
    )

    @classmethod
    def description(cls, context, properties):
        return properties.tooltip
    #END description()


    @classmethod
    def poll(cls, context):
        return True
    #END poll()


    def draw(self, context):
        scn = context.scene
        layout = self.layout.column(align=True)

        #layout.separator()

        enableDisableBtns = layout.row(align=True)
        enableDisableBtns.scale_y = 1.5
        enableDisableBtnsProp = enableDisableBtns.prop(self, "enableDisableToggle", icon="NONE", emboss=True, expand=True)

        layout.separator()

        visibilitySection = layout.column(align=True)
        visibilitySectionInner = visibilitySection.row(align=True)


        btnSection = visibilitySectionInner.box()
        btnRow = btnSection.grid_flow(row_major=True, align=True, columns=2, even_columns=True)
        renderBtn = btnRow.row(align=True)
        renderBtnProp = renderBtn.prop(self, "render", text="")
        label = renderBtn.label(text="Render", icon="RESTRICT_RENDER_OFF")

        realtimeBtn = btnRow.row(align=True)
        renderBtnProp = realtimeBtn.prop(self, "realtime", text="")
        label = realtimeBtn.label(text="Realtime", icon="RESTRICT_VIEW_OFF")

        editModeBtn = btnRow.row(align=True)
        renderBtnProp = editModeBtn.prop(self, "editmode", text="")
        label = editModeBtn.label(text="Edit Mode", icon="EDITMODE_HLT")
        
        cageBtn = btnRow.row(align=True)
        renderBtnProp = cageBtn.prop(self, "cage", text="")
        label = cageBtn.label(text="Cage", icon="OUTLINER_DATA_MESH")
        

        visibilitySectionInner.separator()
        
        resetBtn = visibilitySectionInner.row(align=True)
        resetBtn.active = False
        resetBtn.prop(self, "reset_allVisibilityModes", toggle=True, text="", icon="LOOP_BACK", emboss=False)

        visibilitySection.separator()

        visibilitySectionInner = visibilitySection.row(align=True)

        affectBtn = visibilitySectionInner.row(align=True)
        affectBtnProp = affectBtn.prop(self, "affect", icon="NONE", emboss=True, expand=True)

        visibilitySectionInner.separator()

        resetBtn = visibilitySectionInner.row(align=True)
        resetBtn.active = False
        resetBtn.prop(self, "reset_affect", toggle=True, text="", icon="LOOP_BACK", emboss=False)
    #END draw()


    def execute(self, context):

        propsToReset = [
            ["reset_allVisibilityModes", ["render", "realtime", "editmode", "cage"] ],
            ["reset_affect", ["affect"] ],
        ]

        misc_functions.resetOperatorProps(self, context, propsToReset)

        scn = context.scene

        objs = None #declare

        if self.affect == "SEL":
            objs = misc_functions.getSelObjs(self, context)

        elif self.affect == "ALL":
            objs = misc_functions.getScnObjs(self, context)

        elif self.affect == "UNSEL":
            objs = misc_functions.getUnselObjs(self, context)


        
        for obj in objs:
            for modifier in obj.modifiers:

                if self.enableDisableToggle == "ENABLE":
                    boolResult = True
                elif self.enableDisableToggle == "DISABLE":
                    boolResult = False

                if self.render:
                    if self.enableDisableToggle == "TOGGLE":
                        boolResult = not modifier.show_render

                    modifier.show_render = boolResult

                if self.realtime:
                    if self.enableDisableToggle == "TOGGLE":
                        boolResult = not modifier.show_viewport

                    modifier.show_viewport = boolResult
                
                if self.editmode:
                    if self.enableDisableToggle == "TOGGLE":
                        boolResult = not modifier.show_in_editmode

                    modifier.show_in_editmode = boolResult

                if self.cage:
                    if self.enableDisableToggle == "TOGGLE":
                        boolResult = not modifier.show_on_cage

                    modifier.show_on_cage = boolResult
        
        #final step:
        self.bForcePanelOptions = False

        return {'FINISHED'}
    # END execute()

    
    def invoke(self, context, event):
        scn = context.scene
        
        if self.bForcePanelOptions:

            if scn.ntzbnsutls_mdfrtools.useCustomModifierVisibilitySettings == "CUSTOM":
                
                #prop list
                propList = ['render', 'realtime', 'editmode', "cage"]

                for prop in propList:
                    
                    #get the value of the scene property
                    scnPropVal = getattr(scn.ntzbnsutls_mdfrtools, prop)

                    #set the value of the operator property to the value of the scene property
                    setattr(self, prop, scnPropVal)

        if event.ctrl:
            self.affect = "UNSEL"
        elif event.shift:
            self.affect = "ALL"
        elif event.alt:
            pass
        elif event.oskey:
            pass
        else:
            self.affect = "SEL"

        return self.execute(context)

# END Operator()

class NTZBNSUTLS_OT_applymodifiers(Operator):
    """Tooltip"""
    bl_idname = "ntzbnsutls.applymodifiers"
    bl_label = "Neltulz - Bonus Utils : Apply Modifiers"
    bl_description = "Applies Modifiers.  Default: Selected Objects.  SHIFT: All Objects.  CTRL: Unselected objects"
    bl_options = {'REGISTER', 'UNDO'}

    bForcePanelOptions : BoolProperty (
        name="Force Panel Options",
        description='Gets all of the operator properties from the sidebar panel options.  This will override any settings in the user customized keymap.',
        default = False
    )

    affect_List = [
        ("SEL",       "Selected",   "", "", 0),
        ("ALL",       "All",        "", "", 1),
        ("UNSEL",     "Unselected", "", "", 2),
    ]

    reset_affect : BoolProperty ( name = "Reset Affect", default = False )
    affect : EnumProperty (
        items       = affect_List,
        name        = "Affect",
        description = "Which objects to affect",
        default     = "SEL"
    )

    apply_List = [
        ("ONLY_VISIBLE",          "Only visible & keep hidden",       "Applies only visible modifiers.  Any hidden modifiers will be ignored, and will be kept so that you can unhide and use them later",           "", 0),
        ("VISIBLE_AND_REMOVE",    "Only visible & remove hidden",     "Applies only visible modifiers.  Any hidden modifiers will be removed.  The resulting object(s) will have no modifiers remaining",            "", 1),
        ("ALL",                   "All (Applies hidden)",             "Applies all, which is the blender default.  Any hidden modifiers will be unhidden and applied, which can be seen as unpredictable behavior",  "", 2),
    ]

    reset_apply : BoolProperty ( name = "Reset Apply", default = False )
    apply : EnumProperty (
        items       = apply_List,
        name        = "Apply",
        description = "Which modifiers to apply",
        default     = "VISIBLE_AND_REMOVE"
    )
    

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        scn = context.scene
        layout = self.layout.column(align=True)

        applyRow = layout.row(align=True)
        prop = applyRow.prop(self, 'apply', expand=False)
        applyRow.separator()
        resetPropRow = applyRow.row(align=True)
        resetPropRow.active = False
        resetProp = resetPropRow.prop(self, 'reset_apply', text="", icon="LOOP_BACK", emboss=False)

        layout.separator()

        affectRow = layout.row(align=True)
        affectBtn = affectRow.row(align=True)
        affectBtnProp = affectBtn.prop(self, "affect", icon="NONE", emboss=True, expand=True)

        affectRow.separator()

        resetBtn = affectRow.row(align=True)
        resetBtn.active = False
        resetBtn.prop(self, "reset_affect", toggle=True, text="", icon="LOOP_BACK", emboss=False)
    # END draw()

    def execute(self, context):

        modeAtBegin = "Unknown"
        try:
            #try to determine objectMode
            modeAtBegin = bpy.context.object.mode
        except:
            modeAtBegin = "OBJECT"

        activeObjAtBegin = bpy.context.view_layer.objects.active

        propsToReset = [
            ["reset_apply",  ["apply"] ],
            ["reset_affect", ["affect"] ],
        ]
        

        misc_functions.resetOperatorProps(self, context, propsToReset)

        scn = context.scene

        objs = None #declare

        if self.affect == "SEL":
            objs = misc_functions.getSelObjs(self, context)

        elif self.affect == "ALL":
            objs = misc_functions.getScnObjs(self, context)

        elif self.affect == "UNSEL":
            objs = misc_functions.getUnselObjs(self, context)


        def applyModifier(obj):
            
            if modeAtBegin == "EDIT":
                bpy.ops.object.mode_set(mode='OBJECT')
            
            try:
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier.name)
            except:
                #if a modifier is disabled due to improper settings, remove the modifier
                obj.modifiers.remove(modifier)

            if modeAtBegin == "EDIT":
                bpy.ops.object.mode_set(mode='EDIT')
        
        for obj in objs:
            #set current obj as active obj
            bpy.context.view_layer.objects.active = obj

            for modifier in obj.modifiers:
                
                if self.apply == "ONLY_VISIBLE":
                    if modifier.show_viewport:
                        applyModifier(obj)

                elif self.apply == "VISIBLE_AND_REMOVE":
                    if modifier.show_viewport:
                        applyModifier(obj)
                    else:
                        obj.modifiers.remove(modifier)

                elif self.apply == "ALL":
                    applyModifier(obj)
                    
        
        #set original active object as the active object
        bpy.context.view_layer.objects.active = activeObjAtBegin

        #final step:
        self.bForcePanelOptions = False

        return {'FINISHED'}
    # END execute()



    def invoke(self, context, event):
        scn = context.scene

        if self.bForcePanelOptions:

            if scn.ntzbnsutls_mdfrtools.useCustomModifierVisibilitySettings == "CUSTOM":
                
                #prop list
                propList = ['apply']

                for prop in propList:
                    
                    #get the value of the scene property
                    scnPropVal = getattr(scn.ntzbnsutls_mdfrtools, prop)

                    #set the value of the operator property to the value of the scene property
                    if scnPropVal != "UNSET":
                        setattr(self, prop, scnPropVal)

        if event.ctrl:
            self.affect = "UNSEL"
        elif event.shift:
            self.affect = "ALL"
        elif event.alt:
            pass
        elif event.oskey:
            pass
        else:
            self.affect = "SEL"

        return self.execute(context)
    # END invoke()

# END Operator()


class NTZBNSUTLS_OT_removemodifiers(Operator):
    """Tooltip"""
    bl_idname = "ntzbnsutls.removemodifiers"
    bl_label = "Neltulz - Bonus Utils : Remove Modifiers"
    bl_description = "Remove Modifiers.  Default: Selected Objects.  SHIFT: All Objects.  CTRL: Unselected objects"
    bl_options = {'REGISTER', 'UNDO'}

    affect_List = [
        ("SEL",       "Selected",   "", "", 0),
        ("ALL",       "All",        "", "", 1),
        ("UNSEL",     "Unselected", "", "", 2),
    ]

    reset_affect : BoolProperty( name = "Reset Affect", default = False )
    affect : EnumProperty (
        items       = affect_List,
        name        = "Affect",
        description = "Which objects to affect",
        default     = "SEL"
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        propsToReset = [
            ["reset_affect", ["affect"] ],
        ]

        misc_functions.resetOperatorProps(self, context, propsToReset)
        scn = context.scene

        objs = None #declare

        if self.affect == "SEL":
            objs = misc_functions.getSelObjs(self, context)

        elif self.affect == "ALL":
            objs = misc_functions.getScnObjs(self, context)

        elif self.affect == "UNSEL":
            objs = misc_functions.getUnselObjs(self, context)


        
        for obj in objs:

            for modifier in obj.modifiers:
                obj.modifiers.remove(modifier)

        #final step:
        self.bForcePanelOptions = False

        return {'FINISHED'}
    # END execute()

    def draw(self, context):
        scn = context.scene
        layout = self.layout.column(align=True)

        affectRow = layout.row(align=True)
        affectBtn = affectRow.row(align=True)
        affectBtnProp = affectBtn.prop(self, "affect", icon="NONE", emboss=True, expand=True)

        affectRow.separator()

        resetBtn = affectRow.row(align=True)
        resetBtn.active = False
        resetBtn.prop(self, "reset_affect", toggle=True, text="", icon="LOOP_BACK", emboss=False)
    # END draw()

    def invoke(self, context, event):
        scn = context.scene

        if event.ctrl:
            self.affect = "UNSEL"
        elif event.shift:
            self.affect = "ALL"
        elif event.alt:
            pass
        elif event.oskey:
            pass
        else:
            self.affect = "SEL"

        return self.execute(context)
    # END invoke()

# END Operator()




class NTZBNSUTLS_OT_openmodifiersidebar(Operator):
    """Tooltip"""
    bl_idname = "ntzbnsutls.openmodifiersidebar"
    bl_label = "Neltulz - Bonus Utils : Open Modifier Sidebar"
    bl_description = 'Opens the "Modifiers" sidebar'
    bl_options = {'REGISTER', 'UNDO',
        #'PRESET',
    }

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scn = context.scene

        propertiesAreaFound = False #declare
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'PROPERTIES':
                    area.spaces.active.context = 'MODIFIER'
                    propertiesAreaFound = True

        if not propertiesAreaFound:
            self.report({'ERROR'}, 'Unable to find properties editor.  Please add a properties editor to your user interface and try again.' )

        return {'FINISHED'}
    # END execute()

    def invoke(self, context, event):
        return self.execute(context)
    # END invoke()

# END Operator()