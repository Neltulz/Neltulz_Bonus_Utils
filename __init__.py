bl_info = {
    "name" : "Neltulz - Bonus Utils",
    "author" : "Neil V. Moore",
    "description" : "A collection of miscellaneous bonus utilities",
    "blender" : (2, 81, 0),
    "version" : (1, 0, 1),
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
from . props_misc                 import NTZBNSUTLS_props
from . props_misc                 import NTZBNSUTLS_selcontigedgprops
from . props_misc                 import NTZBNSUTLS_mdfrtoolsprops

#operators
from . ot_selcontigedg            import NTZBNSUTLS_OT_selcontigedg
from . ot_misc                    import NTZBNSUTLS_OT_resetsettings
from . addon_preferences          import NTZBNSUTLS_OT_addonprefs
from . ot_delallunselobjs         import NTZBNSUTLS_OT_delallunselobjs
from . ot_modifiertools           import NTZBNSUTLS_OT_modifiervisibility
from . ot_modifiertools           import NTZBNSUTLS_OT_applymodifiers
from . ot_modifiertools           import NTZBNSUTLS_OT_removemodifiers
from . ot_modifiertools           import NTZBNSUTLS_OT_openmodifiersidebar
from . ot_subdivideplus           import NTZBNSUTLS_OT_subdivideplus
from . ot_offsetfaces             import NTZBNSUTLS_OT_offsetfaces
from . pie_misc                   import NTZBNSUTLS_OT_modifiertoolspie

#panels
from . pt_misc                    import NTZBNSUTLS_PT_selcontigedgoptions
from . pt_misc                    import NTZBNSUTLS_PT_modifiertoolsoptions
from . pt_misc                    import NTZBNSUTLS_PT_sidebarpanel

#pies
from . pie_misc                   import NTZBNSUTLS_MT_modifiertoolspie

#keymaps
from . import keymaps

PendingDeprecationWarning

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
    NTZBNSUTLS_props,
    NTZBNSUTLS_selcontigedgprops,
    NTZBNSUTLS_mdfrtoolsprops,

    #operators
    NTZBNSUTLS_OT_selcontigedg,
    NTZBNSUTLS_OT_resetsettings,
    NTZBNSUTLS_OT_addonprefs,
    NTZBNSUTLS_OT_delallunselobjs,
    NTZBNSUTLS_OT_modifiervisibility,
    NTZBNSUTLS_OT_applymodifiers,
    NTZBNSUTLS_OT_removemodifiers,
    NTZBNSUTLS_OT_openmodifiersidebar,
    NTZBNSUTLS_OT_modifiertoolspie,
    NTZBNSUTLS_OT_subdivideplus,
    NTZBNSUTLS_OT_offsetfaces,

    #panels
    NTZBNSUTLS_PT_selcontigedgoptions,
    NTZBNSUTLS_PT_modifiertoolsoptions,
    NTZBNSUTLS_PT_sidebarpanel,

    #pies
    NTZBNSUTLS_MT_modifiertoolspie,
)

# -----------------------------------------------------------------------------
#    Register classes from the classes list
# -----------------------------------------------------------------------------    

addon_keymaps = []

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

    # update panel name
    prefs = bpy.context.preferences.addons[__name__].preferences
    addon_preferences.update_panel(prefs, bpy.context)

    #add keymaps from keymaps.py
    keymaps.regKM(addon_keymaps)

    #add property group to the scene
    bpy.types.Scene.ntzbnsutls                  = bpy.props.PointerProperty(type=NTZBNSUTLS_props  )
    bpy.types.Scene.ntzbnsutls_selcontigedg     = bpy.props.PointerProperty(type=NTZBNSUTLS_selcontigedgprops)
    bpy.types.Scene.ntzbnsutls_mdfrtools          = bpy.props.PointerProperty(type=NTZBNSUTLS_mdfrtoolsprops)

    #vscode pme workaround from iceythe (part 1 of 2)
    #must be appended to def register() so that it is the last thing that executes
    if bDebugModeActive:
        if not bpy.app.timers.is_registered(_reg):
            bpy.app.timers.register(_reg, first_interval=1)
    #END vscode pme workaround (part 1 of 2)

    


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    #remove keymaps
    keymaps.unregKM(addon_keymaps)



if __name__ == "__main__":
    register()