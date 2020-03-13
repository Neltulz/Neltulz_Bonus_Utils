import bpy

# -----------------------------------------------------------------------------
#    Keymaps (For Register)
# -----------------------------------------------------------------------------    

def regKM(addonKeymaps, wm):

    kc = wm.keyconfigs.addon.keymaps


    #------------------------------3d View ----------------------------------------------------------------------------

    # fetch keymap
    km = kc.get("3D View")

    # create a list for keymap items for current km
    addonKeymaps[km] = []

    #km = wm.keyconfigs.addon.keymaps.new(name = "3D View", space_type="VIEW_3D")

    kmi = km.keymap_items.new("view3d.ntzbu_modifier_tools_pie", type='Q', value='PRESS',
                              ctrl=True, shift=True, alt=False)

    # add keymap item to list
    addonKeymaps[km].append(kmi)


    #km = wm.keyconfigs.addon.keymaps.new(name = "3D View", space_type="VIEW_3D")

    kmi = km.keymap_items.new("view3d.ntzbu_all_in_one_tool_settings", type='Q', value='PRESS',
                              ctrl=False, shift=False, alt=True)

    # add keymap item to list
    addonKeymaps[km].append(kmi)

def unregKM(addonKeymaps, wm):
    # handle the keymap
    for km, km_list in addonKeymaps.items():
        for kmi in km_list:
            km.keymap_items.remove(kmi)
    addonKeymaps.clear()