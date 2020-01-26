import bpy
from . props_misc import NTZBNSUTLS_mdfrtoolsprops

# -----------------------------------------------------------------------------
#    Keymaps (For Register)
# -----------------------------------------------------------------------------    

def regKM(addon_keymaps):
    pass
    wm = bpy.context.window_manager



    #------------------------------3d View (Generic)----------------------------------------------------------------------------

    km = wm.keyconfigs.addon.keymaps.new(name = "3D View Generic", space_type="VIEW_3D")

    kmi = km.keymap_items.new("ntzbnsutls.modifiertoolspie", type='Q', value='PRESS',
                              ctrl=True, shift=True, alt=False)

    #add list of keymaps
    addon_keymaps.append(km)

    #---------------------------------------------------------------------------------------------------------------------------

    km = wm.keyconfigs.addon.keymaps.new(name = "3D View", space_type="VIEW_3D")

    kmi = km.keymap_items.new("ntzbnsutls.aiotoolsettings", type='Q', value='PRESS',
                              ctrl=False, shift=False, alt=True)

    #add list of keymaps
    addon_keymaps.append(km)

def unregKM(addon_keymaps):
    # handle the keymap
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    addon_keymaps.clear()