import bpy

def mainBonusUtilsPanel(self, context, bUseCompactSidebarPanel, bUseCompactPopupAndPiePanel):
    layout = self.layout
    scn = context.scene

    #determine if panel is inside of a popop/pie menu
    panelInsidePopupOrPie = context.region.type == 'WINDOW'

    if panelInsidePopupOrPie:

        if bUseCompactPopupAndPiePanel:
            layout.ui_units_x = 10
            layout.label(text="Bonus Utils")

        else:
            layout.ui_units_x = 13
            layout.label(text="Neltulz - Bonus Utils")

    #-----------------------------------------------------------------------------------------------------------------------------------------------
    # Object Section
    #-----------------------------------------------------------------------------------------------------------------------------------------------

    createShowHide(self, context, scn, "ntzbnsutls", "show_object_section", None, 'Object', layout)

    if scn.ntzbnsutls.show_object_section:
        sectionRow = layout.row(align=True)
        leftIndent = sectionRow.label(text="", icon="BLANK1")
        sectionInner = sectionRow.column(align=True)

        #Delete all Unsel Objs
        btnWithDropdown = sectionInner.row(align=True)
        op = btnWithDropdown.operator("view3d.ntzbu_delete_all_unselected_objs", text="Delete Unselected Objects")

        popover = btnWithDropdown.row(align=True)
        popover.alignment="RIGHT"
        popoverBtn = popover.popover(text="", panel="VIEW3D_PT_ntzbu_delete_all_unselected_objects_options", icon="NONE")

        sectionInner.separator()

        #Group with Empty
        btnWithDropdown = sectionInner.row(align=True)
        op = btnWithDropdown.operator("view3d.ntzbu_group_with_empty", text="Group With Empty")
        op.bUseOverridesFromAddonPrefs = True

        popover = btnWithDropdown.row(align=True)
        popover.alignment="RIGHT"
        popoverBtn = popover.popover(text="", panel="VIEW3D_PT_ntzbu_group_with_empty_options", icon="NONE")

        sectionInner.separator()
        
        #Smart Unparent
        btn = sectionInner.row(align=True)
        op = btn.operator("view3d.ntzbu_smart_unparent", text="Smart Unparent")

        sectionInner.separator()
        
        #Smart Instance Collection
        btn = sectionInner.row(align=True)
        op = btn.operator("view3d.ntzbu_smart_instance_collection", text="Smart Instance Collection")
        

    #-----------------------------------------------------------------------------------------------------------------------------------------------
    # Mesh Section
    #-----------------------------------------------------------------------------------------------------------------------------------------------

    createShowHide(self, context, scn, "ntzbnsutls", "show_meshEditMode_section", None, 'Mesh', layout)

    if scn.ntzbnsutls.show_meshEditMode_section:
        sectionRow = layout.row(align=True)
        leftIndent = sectionRow.label(text="", icon="BLANK1")
        sectionInner = sectionRow.column(align=True)

        #Select Contiguous Edges
        btnWithDropdown = sectionInner.row(align=True)
        op = btnWithDropdown.operator("view3d.ntzbu_select_contiguous_edges", text="Select Contiguous Edges")
        op.bUseOverridesFromAddonPrefs = True

        sectionInner.separator()

        popover = btnWithDropdown.row(align=True)
        popover.alignment="RIGHT"
        popoverBtn = popover.popover(text="", panel="VIEW3D_PT_ntzbu_select_contiguous_edges_options", icon="NONE")

        #Subdivide+
        btnWithDropdown = sectionInner.row(align=True)
        op = btnWithDropdown.operator("view3d.ntzbu_subdivide_plus", text="Subdivide+")

        #Offset All Faces
        btn = sectionInner.operator("view3d.ntzbu_offset_all_faces", text="Offset All Faces")

        #Normal Extrude+
        btn = sectionInner.operator("view3d.ntzbu_normal_extrude_plus", text="Normal Extrude+")

    #-----------------------------------------------------------------------------------------------------------------------------------------------
    # Modifiers Section
    #-----------------------------------------------------------------------------------------------------------------------------------------------

    createShowHide(self, context, scn, "ntzbnsutls", "show_modifiers_section", None, 'Modifiers', layout)

    if scn.ntzbnsutls.show_modifiers_section:
        sectionRow = layout.row(align=True)
        leftIndent = sectionRow.label(text="", icon="BLANK1")
        sectionInner = sectionRow.column(align=True)

        #Modifier Visibility
        btnWithDropdown = sectionInner.row(align=True)
        btnRow = btnWithDropdown.row(align=True)
        op = btnRow.operator("view3d.ntzbu_modifier_visibility", text="Enable")
        op.enableDisableToggle = "ENABLE"
        op.tooltip = "Enable Modifiers.  Default: Selected Objects.  SHIFT: All Objects.  CTRL: Unselected objects"

        op = btnRow.operator("view3d.ntzbu_modifier_visibility", text="Toggle")
        op.enableDisableToggle = "TOGGLE"
        op.tooltip = "Toggle Modifiers.  Default: Selected Objects.  SHIFT: All Objects.  CTRL: Unselected objects"
        
        op = btnRow.operator("view3d.ntzbu_modifier_visibility", text="Disable")
        op.enableDisableToggle = "DISABLE"
        op.tooltip = "Disable Modifiers.  Default: Selected Objects.  SHIFT: All Objects.  CTRL: Unselected objects"

        #Apply / Remove all modifiers
        btnWithDropdown = sectionInner.row(align=True)
        btnRow = btnWithDropdown.row(align=True)
        op = btnRow.operator("view3d.ntzbu_apply_modifiers", text="Apply")

        op = btnRow.operator("view3d.ntzbu_remove_modifiers", text="Remove")

    #-----------------------------------------------------------------------------------------------------------------------------------------------
    # 3D Cursor Section
    #-----------------------------------------------------------------------------------------------------------------------------------------------

    createShowHide(self, context, scn, "ntzbnsutls", "show_3dcursor_section", None, '3D Cursor', layout)

    if scn.ntzbnsutls.show_3dcursor_section:
        sectionRow = layout.row(align=True)
        leftIndent = sectionRow.label(text="", icon="BLANK1")
        sectionInner = sectionRow.column(align=True)

        btnRow = sectionInner.row(align=True)
        op = btnRow.operator("view3d.ntzbu_adjust_3d_cursor", text="Adjust")
        op = btnRow.operator("view3d.ntzbu_apply_3d_cursor", text="Apply")
        op = btnRow.operator("view3d.ntzbu_rotate_3d_cursor", text="Rotate")

        btnRow = sectionInner.row(align=True)
        op = btnRow.operator("view3d.ntzbu_snap_cursor_plus", text="Snap Cursor+")

        

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

def createPropOLD(self, context, scn=None, bEnabled=True, labelText='', data=None, propItem='', scale_y=1, labelScale=5, propScale=20, labelAlign='RIGHT', propAlign='EXPAND', propText='', bExpandProp=False, bUseSlider=False, layout=None):

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

def createProp_or_Op(self, context, lay, scn=None, useOperator=False, enable=True, labelTxt='', labelTxt2=None, labelVOffset=0, labelHeight=1, propName='', propHeight=1, propVOffset=0, labelWidth=7, propWidth=15, labelJustify="RIGHT", propJustify="LEFT", propText=None, bExpandProp=True, toggleProp=False, embossProp=True, op1='', op1Text=None, op1Options=None, op2='', op2Text=None, op2Options=None):

    # Prerequesites:
    if ( propName != '' and not useOperator ) or ( op1 != '' and useOperator ):

        row = lay.row(align=True)
        row.alignment="CENTER"

        if not enable:
            row.enabled = False

        row.scale_y = propHeight

        col1MasterContainer = row.row(align=True)
        col1MasterContainer.alignment="EXPAND"
        col1MasterContainer.ui_units_x = labelWidth

        col1Container = col1MasterContainer.column(align=True)
        col1Container.alignment=labelJustify
        col1Container.scale_x = 1
        col1Container.scale_y = labelHeight

        if labelVOffset > 0:
            col1Container.separator(factor=labelVOffset)

        col1Container.label(text=labelTxt)

        if labelTxt2 is not None:
            col1Container.label(text=labelTxt2)

        col2MasterContainer = row.row(align=True)
        col2MasterContainer.alignment=propJustify

        col2Container = col2MasterContainer.column(align=True)

        if propVOffset > 0:
            vSep = col2Container.row(align=True)
            vSep.ui_units_y = propVOffset
            vSep.label(text=' ')


        col2Container.alignment=propJustify
        col2Container.ui_units_x = propWidth
        col2Container.scale_x = 100

        enableProp = getattr(self, f'{propName}_active', None)

        propRow = col2Container.row(align=True)

        if enableProp is not None:
            if not enableProp:
                propRow2 = propRow.row(align=False)
                propRow3 = propRow2.row(align=True)
                propRow3.active=False
                propRow3.prop(self, propName, text=propText, expand=bExpandProp, toggle=toggleProp, emboss=embossProp)
                propRow2.prop(self, f'{propName}_active', text='', icon='BLANK1', expand=False, toggle=False, emboss=False, invert_checkbox=False)
            else:
                propRow2 = propRow.row(align=False)
                propRow2.prop(self, propName, text=propText, expand=bExpandProp, toggle=toggleProp, emboss=embossProp)
                propRow2.prop(self, f'{propName}_active', text='', icon='X', expand=False, toggle=False, emboss=False, invert_checkbox=False)


        elif useOperator:
            propRow2 = propRow.row(align=True)
            op = propRow2.operator(op1, text=op1Text)
            
            if op1Options is not None:
                for option in op1Options:
                    exec( f'op.{option["propName"]} = {option["propVal"]}' )
            
            if op2 != '':
                op = propRow2.operator(op2, text=op2Text)

                if op2Options is not None:
                    for option in op2Options:
                        exec( f'op.{option["propName"]} = {option["propVal"]}' )
                    
        else:
            propRow2 = propRow.row(align=True)
            propRow2.prop(self, propName, text=propText, expand=bExpandProp)
    else:
        pass

def createPropWithHideButtonAlt(self, context, scn, properties, propName, customPropText, bUseSlider, embossResetBtn, layout):

    propRow = layout.row(align=True)

    data                       = eval( f"scn.{properties}" )


    propCol                    = propRow.column(align=True)
    propCol.prop               ( data, propName, text=customPropText, slider=bUseSlider)

    resetPropCol               = propRow.column(align=True)
    resetPropCol.active        = embossResetBtn
    resetPropOp                = resetPropCol.operator("view3d.ntzbu_reset_settings", text="", icon="LOOP_BACK", emboss=embossResetBtn)
    resetPropOp.settingToReset = propName


def modifierToolsOptions(self, context, scn, layout):

    layout.label(text='Modifiers', icon="MODIFIER")
    layout.separator()
    layout.label(text="Visibility Settings:")

def delUnselObjs_options(self, context, lay=None):

    createProp_or_Op(self, context, lay,
        labelTxt     = 'Use Confirm Dialog',
        propName     = "delUnselObjs_useConfirmDiag",
    )

def groupWithEmpty_options(self, context, lay=None):
    
    createProp_or_Op(self, context, lay,
        labelTxt     = 'Operator Options',
        propName     = "groupWithEmpty_showOperatorOptions",
    )
    
    lay.separator()

    createProp_or_Op(self, context, lay,
        useOperator = True,
        labelTxt    = 'Relationship Lines',
        op1         = 'view3d.ntzbu_toggle_relationship_lines_in_all_3dviews',
        op1Text     = 'Show',
        op1Options  = [{'propName' : 'state', 'propVal' : 'True'}],

        op2         = 'view3d.ntzbu_toggle_relationship_lines_in_all_3dviews',
        op2Text     = 'Hide',
        op2Options  = [{'propName' : 'state', 'propVal' : 'False'}],
    )

    lay.separator()

    createProp_or_Op(self, context, lay,
        labelTxt     = 'Empty Name',
        propText     = '',
        propName     = 'groupWithEmpty_emptyName',
    )

    lay.separator()

    createProp_or_Op(self, context, lay,
        labelTxt     = 'Empty Location',
        propName     = 'groupWithEmpty_emptyLocation',
    )

    lay.separator()

    createProp_or_Op(self, context, lay,
        labelTxt     = 'Empty Size',
        propName     = 'groupWithEmpty_emptySize',
    )
# END groupWithEmpty_options()

def smartInstColl_options(self, context, lay=None):
        createProp_or_Op(self, context, lay,
        labelTxt     = 'Operator Options',
        propName     = "smartInstColl_showOperatorOptions",
    )
# END smartInstColl_options()


def createSectionToggleOperator(self, context, lay=None, data=None, dataStr='NONE', sectionBool='NONE', text='NONE', width=0, height=1):

    boxTitle = lay.row(align=True)

    boxTitle.scale_y = height

    if width > 0:
        boxTitle.alignment='CENTER'

    boxTitle2 = boxTitle.row(align=True)
    
    if width > 0:
        boxTitle2.ui_units_x = width

    showHideProp = getattr(data, sectionBool, None)

    if showHideProp is not None:

        if showHideProp:
            icon = 'TRIA_DOWN_BAR'
        else:
            icon = 'TRIA_RIGHT_BAR'

        op = boxTitle2.operator('wm.ntzbu_toggle_section', text=text, icon=icon)
        op.data = dataStr
        op.group = sectionBool

def forceJustifyText(lay=None, text="", icon='NONE', alignment='CENTER'):
    grid = lay.grid_flow(align=True, columns=1, even_columns=False, row_major=True)

    rowTitle1 = grid.row(align=True)
    rowTitle1.scale_y = 0.0000001
    rowTitle1.alignment="EXPAND"
    rowTitle1.label(text=' ')

    rowTitle2 = grid.row(align=True)
    rowTitle2.alignment=alignment
    rowTitle2.label(text=text, icon=icon)


def selContigEdg_options(self, context, lay=None):

    createProp_or_Op(self, context, lay,
        labelTxt     = 'Max Angle',
        propText     = '',
        propName     = 'selContigEdg_maxAngle',
    )

    lay.separator()

    createProp_or_Op(self, context, lay,
        labelTxt     = 'Max Edges',
        propText     = '',
        propName     = 'selContigEdg_maxEdges',
    )

    lay.separator()

    createProp_or_Op(self, context, lay,
        labelTxt     = 'Direction',
        propName     = 'selContigEdg_direction',
    )