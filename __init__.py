bl_info = {
    "name" : "Neltulz - Bonus Utils",
    "author" : "Neil V. Moore",
    "description" : "A collection of miscellaneous bonus utilities",
    "blender" : (2, 90, 0),
    "version" : (1, 0, 6),
    "location" : "View3D",
    "warning" : "",
    "category" : "3D View",
    "tracker_url": "https://www.logichaos.com/neltulz_blender_addons/neltulz_contact_page/neltulz_contact_page",
    "wiki_url": "https://www.logichaos.com/neltulz_blender_addons/neltulz_bonus_utils/README_Neltulz_Bonus_Utils"
}

# -----------------------------------------------------------------------------
#   Import Classes and/or functions
# -----------------------------------------------------------------------------  

import bpy

#props
from . props                      import ntzbu_props

#operators
from . selcontigedgOt             import VIEW3D_OT_ntzbu_select_contiguous_edges

from . miscOt                     import WM_OT_ntzbu_toggle_section
from . miscOt                     import VIEW3D_OT_ntzbu_reset_settings
from . miscOt                     import VIEW3D_OT_ntzbu_toggle_relationship_lines_in_all_3dviews


from . addonPreferences           import VIEW3D_OT_ntzbu_addon_prefs

from . delallunselobjsOt          import VIEW3D_OT_ntzbu_delete_all_unselected_objs
from . groupWithEmptyOt           import VIEW3D_OT_ntzbu_group_with_empty
from . smartUnparentOt            import VIEW3D_OT_ntzbu_smart_unparent
from . instancecollOt             import VIEW3D_OT_ntzbu_smart_instance_collection

from . modifiertoolsOt            import VIEW3D_OT_ntzbu_modifier_visibility
from . modifiertoolsOt            import VIEW3D_OT_ntzbu_apply_modifiers
from . modifiertoolsOt            import VIEW3D_OT_ntzbu_remove_modifiers
from . modifiertoolsOt            import VIEW3D_OT_ntzbu_open_modifiers_sidebar

from . aiotoolsettingsOt          import VIEW3D_OT_ntzbu_all_in_one_tool_settings
from . subdivideplusOt            import VIEW3D_OT_ntzbu_subdivide_plus
from . offsetfacesOt              import VIEW3D_OT_ntzbu_offset_all_faces
from . normalextrudeplusOt        import VIEW3D_OT_ntzbu_normal_extrude_plus

from . cursorOt                   import VIEW3D_OT_ntzbu_adjust_3d_cursor
from . cursorOt                   import VIEW3D_OT_ntzbu_apply_3d_cursor
from . cursorOt                   import VIEW3D_OT_ntzbu_rotate_3d_cursor
from . cursorOt                   import VIEW3D_OT_ntzbu_snap_cursor_plus

from . pieMisc                    import VIEW3D_OT_ntzbu_modifier_tools_pie

#panels
from . miscPt                     import VIEW3D_PT_ntzbu_delete_all_unselected_objects_options
from . miscPt                     import VIEW3D_PT_ntzbu_group_with_empty_options
from . miscPt                     import VIEW3D_PT_ntzbu_select_contiguous_edges_options
from . miscPt                     import VIEW3D_PT_ntzbu_modifier_tools_options
from . miscPt                     import VIEW3D_PT_ntzbu_sidebar_panel

#pies
from . pieMisc                    import VIEW3D_MT_ntzbu_modifier_tools_pie

#keymaps
from .                            import keymaps

PendingDeprecationWarning

wm = bpy.context.window_manager

bDebugModeActive = False
if bDebugModeActive:
    print("##################################################################################################################################################################")
    print("REMINDER: DEBUG MODE ACTIVE")
    print("##################################################################################################################################################################")

# -----------------------------------------------------------------------------
#    Store classes in List so that they can be easily registered/unregistered    
# -----------------------------------------------------------------------------  

classes = (
    #props
    ntzbu_props,

    #operators
    VIEW3D_OT_ntzbu_select_contiguous_edges,

    WM_OT_ntzbu_toggle_section,
    VIEW3D_OT_ntzbu_reset_settings,
    VIEW3D_OT_ntzbu_toggle_relationship_lines_in_all_3dviews,

    VIEW3D_OT_ntzbu_delete_all_unselected_objs,
    VIEW3D_OT_ntzbu_group_with_empty,
    VIEW3D_OT_ntzbu_smart_unparent,
    VIEW3D_OT_ntzbu_smart_instance_collection,
    VIEW3D_OT_ntzbu_modifier_visibility,
    VIEW3D_OT_ntzbu_apply_modifiers,
    VIEW3D_OT_ntzbu_remove_modifiers,
    VIEW3D_OT_ntzbu_open_modifiers_sidebar,
    VIEW3D_OT_ntzbu_all_in_one_tool_settings,
    VIEW3D_OT_ntzbu_subdivide_plus,
    VIEW3D_OT_ntzbu_offset_all_faces,
    VIEW3D_OT_ntzbu_normal_extrude_plus,
    VIEW3D_OT_ntzbu_adjust_3d_cursor,
    VIEW3D_OT_ntzbu_apply_3d_cursor,
    VIEW3D_OT_ntzbu_rotate_3d_cursor,
    VIEW3D_OT_ntzbu_snap_cursor_plus,
    VIEW3D_OT_ntzbu_modifier_tools_pie,

    #panels
    VIEW3D_PT_ntzbu_delete_all_unselected_objects_options,
    VIEW3D_PT_ntzbu_group_with_empty_options,
    VIEW3D_PT_ntzbu_select_contiguous_edges_options,
    VIEW3D_PT_ntzbu_modifier_tools_options,
    VIEW3D_PT_ntzbu_sidebar_panel,

    #pies
    VIEW3D_MT_ntzbu_modifier_tools_pie,
)

# -----------------------------------------------------------------------------
#    Register classes from the classes list
# -----------------------------------------------------------------------------    

addonKeymaps = []

#vscode pme workaround from iceythe (part 2 of 2)
def _reg():
    pme = bpy.utils._preferences.addons['pie_menu_editor'].preferences
    for pm in pme.pie_menus:
        if pm.key != 'NONE':
            pm.register_hotkey()
#END vscode pme workaround (part 2 of 2)

def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    #register preferences last:
    register_class(VIEW3D_OT_ntzbu_addon_prefs)
    prefs = bpy.context.preferences.addons[__name__].preferences

    
    # update panel name
    addonPreferences.update_panel(prefs, bpy.context)
    

    #add keymaps from keymaps.py
    keymaps.regKM(addonKeymaps)


    #add property group to the scene
    bpy.types.Scene.ntzbnsutls                  = bpy.props.PointerProperty(type=ntzbu_props  )

    #vscode pme workaround from iceythe (part 1 of 2)
    #must be appended to def register() so that it is the last thing that executes
    if bDebugModeActive:
        if not bpy.app.timers.is_registered(_reg):
            bpy.app.timers.register(_reg, first_interval=1)
    #END vscode pme workaround (part 1 of 2)

    


def unregister():
    from bpy.utils import unregister_class

    #unregister preferences first
    unregister_class(VIEW3D_OT_ntzbu_addon_prefs)

    for cls in reversed(classes):
        unregister_class(cls)

    #remove keymaps
    keymaps.unregKM(addonKeymaps)



if __name__ == "__main__":
    register()