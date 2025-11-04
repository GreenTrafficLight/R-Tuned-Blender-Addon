import bpy
import struct

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, PointerProperty
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )

from .Blender.operators.OT_Model_Import import *

bl_info = {
	"name": "R-Tuned Ultimate Street Racing Models format",
	"description": "Import R-Tuned Ultimate Street Racing Model",
	"author": "GreenTrafficLight",
	"version": (1, 1),
	"blender": (4, 0, 0),
	"location": "File > Import > R-Tuned Ultimate Street Racing Importer",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"support": "COMMUNITY",
	"category": "Import-Export"}


classes = [
    RTUNED_OT_Model_Import,
]

# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(RTUNED_OT_Model_Import.bl_idname, text="R-Tuned Ultimate Street Racing")

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
