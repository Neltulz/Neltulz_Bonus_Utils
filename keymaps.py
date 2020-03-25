import bpy

# -----------------------------------------------------------------------------
#    Keymaps (For Register)
# -----------------------------------------------------------------------------    

def regKM(addonKeymaps):

    wm = bpy.context.window_manager

    #------------------------------3d View ----------------------------------------------------------------------------

    km = wm.keyconfigs.addon.keymaps.new(name = "3D View", space_type="VIEW_3D")

    kmi = km.keymap_items.new("view3d.ntzbu_modifier_tools_pie", type='Q', value='PRESS',
                              ctrl=True, shift=True, alt=False)

    kmi = km.keymap_items.new("view3d.ntzbu_all_in_one_tool_settings", type='Q', value='PRESS',
                              ctrl=False, shift=False, alt=True)

    #add list of keymaps
    addonKeymaps.append(km)

def unregKM(addonKeymaps):
    # handle the keymap
    wm = bpy.context.window_manager
    for km in addonKeymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    addonKeymaps.clear()