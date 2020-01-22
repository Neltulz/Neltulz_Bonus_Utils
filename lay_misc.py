import bpy

def mainBonusUtilsPanel(self, context, bUseCompactSidebarPanel, bUseCompactPopupAndPiePanel):
    layout = self.layout
    scn = context.scene

    #determine if panel is inside of a popop/pie menu
    panelInsidePopupOrPie = context.region.type == 'WINDOW'

    if panelInsidePopupOrPie:

        if bUseCompactPopupAndPiePanel:
            layout.ui_units_x = 8
            layout.label(text="Bonus Utils")

        else:
            layout.ui_units_x = 13
            layout.label(text="Neltulz - Bonus Utils")

    createShowHide(self, context, scn, "ntzbnsutls", "show_object_section", None, 'Object', layout)

    if scn.ntzbnsutls.show_object_section:
        sectionRow = layout.row(align=True)
        leftIndent = sectionRow.label(text="", icon="BLANK1")
        sectionInner = sectionRow.column(align=True)

        #Delete all Unsel Objs
        btn = sectionInner.operator("ntzbnsutls.delallunselobjs", text="Delete Unselected Objects")
        


    createShowHide(self, context, scn, "ntzbnsutls", "show_meshEditMode_section", None, 'Mesh', layout)

    if scn.ntzbnsutls.show_meshEditMode_section:
        sectionRow = layout.row(align=True)
        leftIndent = sectionRow.label(text="", icon="BLANK1")
        sectionInner = sectionRow.column(align=True)

        #Select Contiguous Edges
        btnWithDropdown = sectionInner.row(align=True)
        op = btnWithDropdown.operator("ntzbnsutls.selcontigedg", text="Select Contiguous Edges")
        if scn.ntzbnsutls_selcontigedg.useCustomSettings == "CUSTOM": op.bForcePanelOptions = True

        sectionInner.separator()

        popover = btnWithDropdown.row(align=True)
        popover.alignment="RIGHT"
        popoverBtn = popover.popover(text="", panel="NTZBNSUTLS_PT_selcontigedgoptions", icon="NONE")

        #sectionInner.separator()

        #Subdivide+
        btnWithDropdown = sectionInner.row(align=True)
        op = btnWithDropdown.operator("ntzbnsutls.subdivideplus", text="Subdivide+")

        '''
        popover = btnWithDropdown.row(align=True)
        popover.alignment="RIGHT"
        popoverBtn = popover.popover(text="", panel="NTZBNSUTLS_PT_selcontigedgoptions", icon="NONE")
        '''

        #Offset Faces
        btn = sectionInner.operator("ntzbnsutls.offsetfaces", text="Offset Faces")

    createShowHide(self, context, scn, "ntzbnsutls", "show_modifiers_section", None, 'Modifiers', layout)

    if scn.ntzbnsutls.show_modifiers_section:
        sectionRow = layout.row(align=True)
        leftIndent = sectionRow.label(text="", icon="BLANK1")
        sectionInner = sectionRow.column(align=True)

        #Modifier Visibility
        btnWithDropdown = sectionInner.row(align=True)
        btnRow = btnWithDropdown.row(align=True)
        op = btnRow.operator("ntzbnsutls.modifiervisibility", text="Enable")
        op.enableDisableToggle = "ENABLE"
        if scn.ntzbnsutls_mdfrtools.useCustomModifierVisibilitySettings == "CUSTOM": op.bForcePanelOptions = True
        op.tooltip = "Enable Modifiers.  Default: Selected Objects.  SHIFT: All Objects.  CTRL: Unselected objects"

        op = btnRow.operator("ntzbnsutls.modifiervisibility", text="Toggle")
        op.enableDisableToggle = "TOGGLE"
        if scn.ntzbnsutls_mdfrtools.useCustomModifierVisibilitySettings == "CUSTOM": op.bForcePanelOptions = True
        op.tooltip = "Toggle Modifiers.  Default: Selected Objects.  SHIFT: All Objects.  CTRL: Unselected objects"
        
        op = btnRow.operator("ntzbnsutls.modifiervisibility", text="Disable")
        op.enableDisableToggle = "DISABLE"
        if scn.ntzbnsutls_mdfrtools.useCustomModifierVisibilitySettings == "CUSTOM": op.bForcePanelOptions = True
        op.tooltip = "Disable Modifiers.  Default: Selected Objects.  SHIFT: All Objects.  CTRL: Unselected objects"


        popover = btnWithDropdown.row(align=True)
        popover.alignment="RIGHT"
        popoverBtn = popover.popover(text="", panel="NTZBNSUTLS_PT_modifiertoolsoptions", icon="NONE")

        #Apply / Remove all modifiers
        btnWithDropdown = sectionInner.row(align=True)
        btnRow = btnWithDropdown.row(align=True)
        op = btnRow.operator("ntzbnsutls.applymodifiers", text="Apply")
        if scn.ntzbnsutls_mdfrtools.useCustomModifierApplySettings == "CUSTOM": op.bForcePanelOptions = True

        op = btnRow.operator("ntzbnsutls.removemodifiers", text="Remove")

#Show hide section with arrow, optional checkbox, and text
def createShowHide(self, context, scn, properties, showHideBool, optionalCheckboxBool, text, layout):

    if scn is not None:
        data = eval( f"scn.{properties}" )
        boolThing = eval( f"scn.{properties}.{showHideBool}" )
    else:
        data = self
        boolThing = eval( f"self.{showHideBool}")

    if boolThing:
        showHideIcon = "TRIA_DOWN"
    else:
        showHideIcon = "TRIA_RIGHT"

    row = layout.row(align=True)

    downArrow = row.column(align=True)
    downArrow.alignment = "LEFT"
    downArrow.prop(data, showHideBool, text="", icon=showHideIcon, emboss=False )

    if optionalCheckboxBool is not None:
        checkbox = row.column(align=True)
        checkbox.alignment = "LEFT"
        checkbox.prop(data, optionalCheckboxBool, text="" )

    textRow = row.column(align=True)
    textRow.alignment = "LEFT"
    textRow.prop(data, showHideBool, text=text, emboss=False )

    emptySpace = row.column(align=True)
    emptySpace.alignment = "EXPAND"
    emptySpace.prop(data, showHideBool, text=" ", emboss=False)


def createProp(self, context, scn, bEnabled, labelText, data, propItem, scale_y, labelScale, propScale, labelAlign, propAlign, propText, bExpandProp, bUseSlider, layout):

    propRow = layout.row(align=True)

    if not bEnabled:
        propRow.enabled = False

    propRow.scale_y = scale_y

    propRowLabel = propRow.row(align=True)
    propRowLabel.alignment="EXPAND"
    propRowLabel.ui_units_x = labelScale

    propRowLabel1 = propRowLabel.row(align=True)
    propRowLabel1.alignment=labelAlign
    propRowLabel1.scale_x = 1

    propRowLabel1.label(text=labelText)

    propRowItem = propRow.row(align=True)
    propRowItem.alignment=propAlign

    propRowItem1 = propRowItem.row(align=True)
    propRowItem1.alignment=propAlign
    propRowItem1.ui_units_x = propScale
    propRowItem1.scale_x = 100

    propRowItem1.prop(data, propItem, text=propText, expand=bExpandProp, slider=bUseSlider)

def createPropWithHideButtonAlt(self, context, scn, properties, propName, customPropText, bUseSlider, embossResetBtn, layout):

    propRow = layout.row(align=True)

    data                       = eval( f"scn.{properties}" )


    propCol                    = propRow.column(align=True)
    propCol.prop               ( data, propName, text=customPropText, slider=bUseSlider)

    resetPropCol               = propRow.column(align=True)
    resetPropCol.active        = embossResetBtn
    resetPropOp                = resetPropCol.operator("ntzbnsutls.resetsettings", text="", icon="LOOP_BACK", emboss=embossResetBtn)
    resetPropOp.settingToReset = propName

def modifierToolsOptions(self, context, scn, layout):

    layout.label(text='Modifiers', icon="MODIFIER")
    layout.separator()
    layout.label(text="Visibility Settings:")
    useCustomVisibilitySettings = layout.prop(scn.ntzbnsutls_mdfrtools, "useCustomModifierVisibilitySettings", text="")

    if scn.ntzbnsutls_mdfrtools.useCustomModifierVisibilitySettings == "CUSTOM":
        settingsBox = layout.box()

        settingsCol = settingsBox.column(align=True)

        visibilitySectionInner = settingsCol.row(align=True)


        btnSection = visibilitySectionInner.box()
        btnRow = btnSection.grid_flow(row_major=True, align=True, columns=2, even_columns=True)
        renderBtn = btnRow.row(align=True)
        renderBtnProp = renderBtn.prop(scn.ntzbnsutls_mdfrtools, "render", text="")
        label = renderBtn.label(text="Render", icon="RESTRICT_RENDER_OFF")

        realtimeBtn = btnRow.row(align=True)
        renderBtnProp = realtimeBtn.prop(scn.ntzbnsutls_mdfrtools, "realtime", text="")
        label = realtimeBtn.label(text="Realtime", icon="RESTRICT_VIEW_OFF")

        editModeBtn = btnRow.row(align=True)
        renderBtnProp = editModeBtn.prop(scn.ntzbnsutls_mdfrtools, "editmode", text="")
        label = editModeBtn.label(text="Edit Mode", icon="EDITMODE_HLT")
        
        cageBtn = btnRow.row(align=True)
        renderBtnProp = cageBtn.prop(scn.ntzbnsutls_mdfrtools, "cage", text="")
        label = cageBtn.label(text="Cage", icon="OUTLINER_DATA_MESH")

        visibilitySectionInner.separator()
        
        resetBtn = visibilitySectionInner.row(align=True)
        resetBtn.active = False
        resetBtnOp = resetBtn.operator('ntzbnsutls.resetsettings', text="", icon="LOOP_BACK", emboss=False)
        resetBtnOp.settingsPropList = "MDFRTOOLS"
        resetBtnOp.mdfrtools_settingsToReset = {"render", "realtime", "editmode", "cage"}

    

    layout.separator()

    layout.label(text="Apply Settings:")
    useCustomApplySettings = layout.prop(scn.ntzbnsutls_mdfrtools, "useCustomModifierApplySettings", text="")

    if scn.ntzbnsutls_mdfrtools.useCustomModifierApplySettings == "CUSTOM":
        settingsBox = layout.box()

        settingsCol = settingsBox.column(align=True)

        applySectionInner = settingsCol.row(align=True)

        applyRow = applySectionInner.row(align=True)

        applyRow.prop(scn.ntzbnsutls_mdfrtools, "apply")

        applyRow.separator()

        resetBtn = applyRow.row(align=True)
        resetBtn.active = False
        resetBtnOp = resetBtn.operator('ntzbnsutls.resetsettings', text="", icon="LOOP_BACK", emboss=False)
        resetBtnOp.settingsPropList = "MDFRTOOLS"
        resetBtnOp.mdfrtools_settingsToReset = {"apply"}

def selContigEdgesSettings(self, context, scn, layout):


    layout.label(text='Select Contiguous Edges', icon="SNAP_MIDPOINT")
    layout.separator()
    layout.label(text='Settings:')
    useCustomSettings = layout.prop(scn.ntzbnsutls_selcontigedg, "useCustomSettings", text="")

    if scn.ntzbnsutls_selcontigedg.useCustomSettings == "CUSTOM":
        settingsBox = layout.box()

        settingsCol = settingsBox.column(align=True)

        maxAngleRow = settingsCol.row(align=True)
        maxAngleProp = maxAngleRow.prop(scn.ntzbnsutls_selcontigedg, "maxAngle", slider=True)
        maxAngleRow.separator()
        resetBtn = maxAngleRow.row(align=True)
        resetBtn.active = False
        resetBtnOp = resetBtn.operator('ntzbnsutls.resetsettings', text="", icon="LOOP_BACK", emboss=False)
        resetBtnOp.settingsPropList = "SELCONTIGEDG"
        resetBtnOp.selcontigedg_settingsToReset = {"maxAngle"}

        maxEdgesRow = settingsCol.row(align=True)
        maxEdgesProp = maxEdgesRow.prop(scn.ntzbnsutls_selcontigedg, "maxEdges", slider=True)
        maxEdgesRow.separator()
        resetBtn = maxEdgesRow.row(align=True)
        resetBtn.active = False
        resetBtnOp = resetBtn.operator('ntzbnsutls.resetsettings', text="", icon="LOOP_BACK", emboss=False)
        resetBtnOp.settingsPropList = "SELCONTIGEDG"
        resetBtnOp.selcontigedg_settingsToReset = {"maxEdges"}

        settingsCol.separator()

        directionRow = settingsCol.row(align=True)
        directionProp = directionRow.prop(scn.ntzbnsutls_selcontigedg, "direction", expand=True)
        directionRow.separator()
        resetBtn = directionRow.row(align=True)
        resetBtn.active = False
        resetBtnOp = resetBtn.operator('ntzbnsutls.resetsettings', text="", icon="LOOP_BACK", emboss=False)
        resetBtnOp.settingsPropList = "SELCONTIGEDG"
        resetBtnOp.selcontigedg_settingsToReset = {"direction"}

        settingsCol.separator()

        resetAllSettingsBtn = settingsCol.row(align=True)
        resetAllSettingsBtn.alignment="CENTER"
        resetAllSettingsOp = resetAllSettingsBtn.operator('ntzbnsutls.resetsettings', text="Reset All Settings", icon="LOOP_BACK")
        resetAllSettingsOp.settingsPropList = "SELCONTIGEDG"
        resetAllSettingsOp.selcontigedg_settingsToReset = {"maxAngle", "maxEdges", "direction"}
