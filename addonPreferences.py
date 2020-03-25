# Update "Tab Category Name" inspired by "Meta-Androcto's" "Edit Mesh Tools" Add-on
# recommended by "cytoo"

import bpy
from rna_keymap_ui import draw_kmi

from . miscPt import VIEW3D_PT_ntzbu_sidebar_panel

from . import miscLay
from . import miscFunc

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# Define Panel classes for updating
panels = (
        VIEW3D_PT_ntzbu_sidebar_panel,
        )

        

def update_panel(self, context):

    addonPrefs = context.preferences.addons[__package__].preferences

    message = "Neltulz - Edge Curve: Updating Panel locations has failed"
    try:
        for panel in panels:
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)

        #Whatever the user typed into the text box in the add-ons settings, set that as the addon's tab category name
        for panel in panels:
            
            if addonPrefs.sbPnlSize == "HIDE":
                panel.bl_category = ""
                panel.bl_region_type = "WINDOW"

            else:
                if addonPrefs.sbPnlSize == "DEFAULT":
                    panel.bUseCompactSidebarPanel = False
                else:
                    panel.bUseCompactSidebarPanel = True

                panel.bl_category = addonPrefs.category
                panel.bl_region_type = "UI"

            if addonPrefs.popPiePnlSize == "DEFAULT":
                panel.bUseCompactPopupAndPiePanel = False
            else:
                panel.bUseCompactPopupAndPiePanel = True

            bpy.utils.register_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__package__, message, e))
        pass



class VIEW3D_OT_ntzbu_addon_prefs(AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    preventInfiniteRecursion : BoolProperty (default=False)

    navTabs_List = [
        ("UILAY",      "UI Layout",  "", "MENU_PANEL",       0),
        ("KM",         "Keymaps",    "", "KEYINGSET",        1),
        ("OBJ",        "Object",     "", "OBJECT_ORIGIN",    2),
        ("MESH",       "Mesh",       "", "OUTLINER_OB_MESH", 3),
        #("MDFRS",      "Modifiers",  "", "MODIFIER",         4),
        #("CURS",       "3D Cursor",  "", "CURSOR",           5),
    ]

    navTabs : EnumProperty (
        items       = navTabs_List,
        name        = "Navigation Tabs",
        default     = "OBJ",
    )

    category: StringProperty(
        name="Tab Category",
        description="Choose a name for the category of the panel",
        default="Neltulz",
        update=update_panel,
    )
        
    sbPnlSize_List = [
        ("DEFAULT", "Default", "", "", 0),
        #("COMPACT", "Compact", "", "", 1),
        ("HIDE",    "Hide",    "", "", 2),
    ]

    sbPnlSize : EnumProperty (
        items       = sbPnlSize_List,
        name        = "Sidebar Panel Size",
        description = "Sidebar Panel Size",
        default     = "DEFAULT",
        update=update_panel,
    )

    popPiePnlSize_List = [
        ("DEFAULT", "Default", "", "", 0),
        ("COMPACT", "Compact", "", "", 1),
    ]

    popPiePnlSize : EnumProperty (
        items       = popPiePnlSize_List,
        name        = "Popup & Pie Panel Size",
        description = "Popup & Pie Panel Size",
        default     = "COMPACT",
        update=update_panel,
    )

    show_AIOToolSettings_addonPrefs : BoolProperty (
        name        = "Show All-in-One Tool Settings Add-on Preferences",
        default     = True,
    )

    aioToolSettings_showOKButton_List = [
        ("YES",             "Yes",         "",          "", 0),
        ("NO",              "No",          "",          "", 1),
    ]

    aioToolSettings_showOKButton : EnumProperty (
        items       = aioToolSettings_showOKButton_List,
        name        = "Show OK Button",
        description = 'Adds an "OK" button to the popup.  Pro: prevents the popup from disappearing until you explicitly click OK or click outside of the popup.  Con: Requires an extra click',
        default     = "NO",
    )

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #    Delete Unselected Objects
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    show_deleteUnselObjs_addonPrefs : BoolProperty (
        name        = 'Show "Delete Unselected Objects" Add-on Preferences',
        default     = True,
    )

    delUnselObjs_useConfirmDiag_List = [
        ("YES",             "Yes",         "",          "", 0),
        ("NO",              "No",          "",          "", 1),
    ]

    delUnselObjs_useConfirmDiag : EnumProperty (
        items       = delUnselObjs_useConfirmDiag_List,
        name        = 'Use Confirm Dialog',
        description = 'Prevents you from causing "Instant Chaos" by prompting you before deleting all unselected objects',
        default     = "YES",
    )

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #    Group With Empty
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    show_groupWithEmpty_addonPrefs : BoolProperty (
        name        = 'Show "Group with Empty" Add-on Preferences',
        default     = True,
    )

    groupWithEmpty_showOperatorOptions_List = [
        ("EXPAND",             "Expand",         "",          "", 0),
        ("COLLAPSE",           "Collapse",       "",          "", 1),
    ]

    groupWithEmpty_showOperatorOptions : EnumProperty (
        items       = groupWithEmpty_showOperatorOptions_List,
        name        = 'Show Operator Options',
        description = 'Shows additional operator options',
        default     = "COLLAPSE",
    )

    def groupWithEmpty_emptyName_deactivate(self, context):
        miscFunc.deactivateProp(self, context, propName='groupWithEmpty_emptyName')

    def groupWithEmpty_emptyName_activate(self, context):
        miscFunc.activateProp(self, context, propName='groupWithEmpty_emptyName')

    groupWithEmpty_emptyName_active : BoolProperty (
        name        = 'Deactivate & Reset "Empty Name"',
        default     = False,
        update      = groupWithEmpty_emptyName_deactivate,
    )

    groupWithEmpty_emptyName : StringProperty (
        name        = 'Empty Name',
        default     = "Group",
        update      = groupWithEmpty_emptyName_activate
    )

    def groupWithEmpty_emptyLocation_deactivate(self, context):
        miscFunc.deactivateProp(self, context, propName='groupWithEmpty_emptyLocation')

    def groupWithEmpty_emptyLocation_activate(self, context):
        miscFunc.activateProp(self, context, propName='groupWithEmpty_emptyLocation')

    groupWithEmpty_emptyLocation_active : BoolProperty (
        name        = 'Deactivate & Reset "Empty Location"',
        default     = False,
        update      = groupWithEmpty_emptyLocation_deactivate,
    )

    groupWithEmpty_emptyLocation_List = [
        ("MEDIAN_POINT",             "Median",         "Median Point",          "", 0),
        ("BOUNDING_BOX_CENTER",      "Bound",          "Bounding Box Center",   "", 1),
        ("ACTIVE_ELEMENT",           "Active",         "Active Element",        "", 2),
        ("WORIGIN",                  "Origin",         "World Orign",           "", 3),
    ]

    groupWithEmpty_emptyLocation : EnumProperty (
        items       = groupWithEmpty_emptyLocation_List,
        name        = "Empty Location",
        default     = "MEDIAN_POINT",
        update      = groupWithEmpty_emptyLocation_activate,
    )



    def groupWithEmpty_emptySize_deactivate(self, context):
        miscFunc.deactivateProp(self, context, propName='groupWithEmpty_emptySize')

    def groupWithEmpty_emptySize_activate(self, context):
        miscFunc.activateProp(self, context, propName='groupWithEmpty_emptySize')

    groupWithEmpty_emptySize_active : BoolProperty (
        name        = 'Deactivate & Reset "Empty Size"',
        default     = False,
        update      = groupWithEmpty_emptySize_deactivate,
    )

    groupWithEmpty_emptySize_List = [
        ("1",      "1",         "",   "", 0),
        ("0.01",   "0.01",      "",   "", 1),
        ("0.0001", "0.0001",    "",   "", 2),
    ]

    groupWithEmpty_emptySize : EnumProperty (
        items       = groupWithEmpty_emptySize_List,
        name        = "Empty Location",
        default     = "0.01",
        update      = groupWithEmpty_emptySize_activate,
    )

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #    Smart Instance Collection
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    show_smartInstColl_addonPrefs : BoolProperty (
        name        = 'Show "Smart Instance Collection" Add-on Preferences',
        default     = True,
    )

    smartInstColl_showOperatorOptions_List = [
        ("EXPAND",             "Expand",         "",          "", 0),
        ("COLLAPSE",           "Collapse",       "",          "", 1),
    ]

    smartInstColl_showOperatorOptions : EnumProperty (
        items       = smartInstColl_showOperatorOptions_List,
        name        = 'Show Operator Options',
        description = 'Shows additional operator options',
        default     = "EXPAND",
    )

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #    Select Contiguous Edges
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    show_selContigEdg_addonPrefs : BoolProperty (
        name        = 'Show "Select Contiguous Edges" Add-on Preferences',
        default     = True,
    )

    def selContigEdg_maxAngle_deactivate(self, context):
        miscFunc.deactivateProp(self, context, propName='selContigEdg_maxAngle')

    def selContigEdg_maxAngle_activate(self, context):
        miscFunc.activateProp(self, context, propName='selContigEdg_maxAngle')

    selContigEdg_maxAngle_active : BoolProperty (
        name        = 'Deactivate & Reset "Max Angle"',
        default     = False,
        update      = selContigEdg_maxAngle_deactivate,
    )

    selContigEdg_maxAngle : IntProperty (
        name        = "Max Angle",
        default     = 15,
        min         = 0,
        max         = 360,
        update      = selContigEdg_maxAngle_activate
    )

    def selContigEdg_maxEdges_deactivate(self, context):
        miscFunc.deactivateProp(self, context, propName='selContigEdg_maxEdges')

    def selContigEdg_maxEdges_activate(self, context):
        miscFunc.activateProp(self, context, propName='selContigEdg_maxEdges')

    selContigEdg_maxEdges_active : BoolProperty (
        name        = 'Deactivate & Reset "Max Edges"',
        default     = False,
        update      = selContigEdg_maxEdges_deactivate,
    )

    selContigEdg_maxEdges : IntProperty(
        name        = "Max Edges",
        default     = 0,
        min         = 0,
        soft_max    = 50,
        update      = selContigEdg_maxEdges_activate,
    )

    def selContigEdg_direction_deactivate(self, context):
        miscFunc.deactivateProp(self, context, propName='selContigEdg_direction')

    def selContigEdg_direction_activate(self, context):
        miscFunc.activateProp(self, context, propName='selContigEdg_direction')

    selContigEdg_direction_active : BoolProperty (
        name        = 'Deactivate & Reset "Direction"',
        default     = False,
        update      = selContigEdg_direction_deactivate,
    )

    selContigEdg_direction_List = (
        ('BACKWARD', "Backward", "", "", 0),
        ('BOTH',     "Both",     "", "", 1),
        ('FORWARD',  "Forward",  "", "", 2),
    )

    selContigEdg_direction : EnumProperty (
        items			= selContigEdg_direction_List,
        name			= "Direction",
        description		= "Search Direction",
        default			= 'BOTH',
        update          = selContigEdg_direction_activate,
    )


    def draw(self, context):

        lay = self.layout.column(align=True)

        if self.sbPnlSize == "HIDE":
            bTabCatEnabled = False
        else:
            bTabCatEnabled = True

        navRow = lay.row(align=True)
        navRow.scale_y = 1.25
        navRow.prop(self, 'navTabs', expand=True)

        


        if self.navTabs == "UILAY":

            box = lay.box().column(align=True)

            box2 = box.row(align=False)
            spacer = box2.row(align=True)

            boxInner = box2.column(align=True)
            rightSpacer = box2.row(align=True)

            boxInner.separator()

            section = boxInner.column(align=True)
        
            miscLay.createProp_or_Op(self, context, section,
                labelTxt     = "Sidebar Panel",
                propName     = "sbPnlSize",
            )

            section.separator()

            miscLay.createProp_or_Op(self, context, section,
                labelTxt     = "Tab Category",
                propName     = "category",
                propText     = "",
            )
            
            section.separator()

            miscLay.createProp_or_Op(self, context, section,
                labelTxt     = "Popup & Pie Panel",
                propName     = "popPiePnlSize",
            )

            boxInner.separator()
            boxInner.separator()
        
            section = boxInner.column(align=True)

            miscLay.createSectionToggleOperator(self, context, 
                lay         = section,
                height      = 1.25,
                data        = self, 
                dataStr     = 'addonPrefs', 
                sectionBool = 'show_AIOToolSettings_addonPrefs', 
                text        = 'All-in-One - Tool Settings Popup'
            )


            if self.show_AIOToolSettings_addonPrefs:
                
                sectionBox = section.box().column(align=True)

                miscLay.createProp_or_Op(self, context, sectionBox,
                    labelTxt     = "Show OK Button",
                    propName     = "aioToolSettings_showOKButton",
                )

            boxInner.separator()
            

        elif self.navTabs == "KM":
            
            box = lay.box().column()

            miscLay.forceJustifyText(lay=box, text='To customize these keymaps, go to your keymaps', icon='QUESTION')
            miscLay.forceJustifyText(lay=box, text='tab on the left and do a search for "NTZBU"')
           
            box.separator()

            miscLay.forceJustifyText(lay=box, text='If your keymaps are not working,')
            miscLay.forceJustifyText(lay=box, text='check for conflicting add-ons and keymaps.')

            #--------------------------------------------------------------------------------
            # NTZBU : Headers
            #--------------------------------------------------------------------------------
            row = lay.grid_flow(align=True, row_major=True, columns=2, even_columns=True)

            rowTitleContainer = row.box().column(align=True)
            rowTitle1 = rowTitleContainer.row(align=True)
            rowTitle1.scale_y = 0.0000001
            rowTitle1.alignment="EXPAND"
            rowTitle1.label(text=' ')
            rowTitle2 = rowTitleContainer.row(align=True)
            rowTitle2.alignment="CENTER"

            rowTitle2.label(text='Operator')

            rowKeybindContainer = row.box().column(align=True)
            keybind1 = rowKeybindContainer.row(align=True)
            keybind1.scale_y = 0.0000001
            keybind1.alignment="EXPAND"
            keybind1.label(text=' ')
            
            keybind2 = rowKeybindContainer.row(align=True)
            keybind2.alignment="CENTER"
            keybind2.label(text='Default Keyboard Shortcut')

            #--------------------------------------------------------------------------------
            # NTZBU : All-in-One Tool Settings
            #--------------------------------------------------------------------------------
            row = lay.grid_flow(align=True, row_major=True, columns=2, even_columns=True)
            
            rowTitleContainer = row.box().column(align=True)
            rowTitle1 = rowTitleContainer.row(align=True)
            rowTitle1.scale_y = 0.0000001
            rowTitle1.alignment="EXPAND"
            rowTitle1.label(text=' ')
            rowTitle2 = rowTitleContainer.row(align=True)
            rowTitle2.alignment="CENTER"

            rowTitle2.label(text='NTZBU : All-in-One Tool Settings')

            rowKeybindContainer = row.box().column(align=True)
            keybind1 = rowKeybindContainer.row(align=True)
            keybind1.scale_y = 0.0000001
            keybind1.alignment="EXPAND"
            keybind1.label(text=' ')
            
            keybind2 = rowKeybindContainer.row(align=True)
            keybind2.alignment="CENTER"
            keybind2.label(text='ALT + Q')
            
            #--------------------------------------------------------------------------------
            # NTZBU : Modifier Tools Pie
            #--------------------------------------------------------------------------------

            row = lay.grid_flow(align=True, row_major=True, columns=2, even_columns=True)
            
            rowTitleContainer = row.box().column(align=True)
            rowTitle1 = rowTitleContainer.row(align=True)
            rowTitle1.scale_y = 0.0000001
            rowTitle1.alignment="EXPAND"
            rowTitle1.label(text=' ')
            rowTitle2 = rowTitleContainer.row(align=True)
            rowTitle2.alignment="CENTER"

            rowTitle2.label(text='NTZBU : Modifier Tools Pie')

            rowKeybindContainer = row.box().column(align=True)
            keybind1 = rowKeybindContainer.row(align=True)
            keybind1.scale_y = 0.0000001
            keybind1.alignment="EXPAND"
            keybind1.label(text=' ')
            
            keybind2 = rowKeybindContainer.row(align=True)
            keybind2.alignment="CENTER"
            keybind2.label(text='SHIFT + CTRL + Q')

            

        elif self.navTabs == "OBJ":

            box = lay.box().column(align=True)

            box2 = box.row(align=False)
            spacer = box2.row(align=True)

            boxInner = box2.column(align=True)
            rightSpacer = box2.row(align=True)

            boxInner.separator()

            section = boxInner.column(align=True)

            miscLay.createSectionToggleOperator(self, context, 
                lay         = section,
                height      = 1.25,
                data        = self, 
                dataStr     = 'addonPrefs', 
                sectionBool = 'show_deleteUnselObjs_addonPrefs', 
                text        = 'Delete Unselected Objects'
            )

            if self.show_deleteUnselObjs_addonPrefs:
                
                sectionBox = section.box()

                miscLay.delUnselObjs_options(self, context, lay=sectionBox)

            boxInner.separator() 

            section = boxInner.column(align=True)

            section.separator()

            miscLay.createSectionToggleOperator(self, context, 
                lay         = section,
                height      = 1.25,
                data        = self, 
                dataStr     = 'addonPrefs', 
                sectionBool = 'show_groupWithEmpty_addonPrefs', 
                text        = 'Group with Empty'
            )

            if self.show_groupWithEmpty_addonPrefs:

                sectionBox = section.box().column(align=True)

                miscLay.groupWithEmpty_options(self, context, lay=sectionBox)

            boxInner.separator()

            section = boxInner.column(align=True)

            section.separator()

            miscLay.createSectionToggleOperator(self, context, 
                lay         = section,
                height      = 1.25,
                data        = self, 
                dataStr     = 'addonPrefs', 
                sectionBool = 'show_smartInstColl_addonPrefs', 
                text        = 'Smart Instance Collection'
            )

            if self.show_smartInstColl_addonPrefs:

                sectionBox = section.box().column(align=True)

                miscLay.smartInstColl_options(self, context, lay=sectionBox)

            boxInner.separator()



        elif self.navTabs == "MESH":
            box = lay.box().column(align=True)

            box2 = box.row(align=False)
            spacer = box2.row(align=True)

            boxInner = box2.column(align=True)
            rightSpacer = box2.row(align=True)

            boxInner.separator()

            section = boxInner.column(align=True)

            miscLay.createSectionToggleOperator(self, context, 
                lay         = section,
                height      = 1.25,
                data        = self, 
                dataStr     = 'addonPrefs', 
                sectionBool = 'show_selContigEdg_addonPrefs', 
                text        = 'Select Contiguous Edges'
            )

            if self.show_selContigEdg_addonPrefs:

                sectionBox = section.box().column(align=True)

                miscLay.selContigEdg_options(self, context, lay=sectionBox)

            boxInner.separator()

        elif self.navTabs == "MDFRS":
            box = lay.box().column(align=True)

            box.label(text="No Options")

        elif self.navTabs == "CURS":
            box = lay.box().column(align=True)

            box.label(text="No Options")



