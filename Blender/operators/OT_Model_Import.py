import bpy

from bpy.types import Operator
from bpy.props import (
        BoolProperty,
        EnumProperty,
        FloatProperty,
        StringProperty,
        CollectionProperty,
        )
from bpy_extras.io_utils import (
        ImportHelper,
        ExportHelper,
        )

from ...Utilities import *
from ..utils.ImportModelRTuned import *

class RTUNED_OT_Model_Import(bpy.types.Operator):
    """Load R-Tuned folder"""
    bl_idname = "import_rtuned.data"
    bl_label = "Import R-Tuned Ultimate Street Racing folder"
    bl_options = {'REGISTER', 'UNDO'}

    directory: StringProperty(
        name="Directory",
        description="Select folder containing geometry.bin + object.bin",
        subtype='DIR_PATH'
    )

    clear_scene: BoolProperty(
        name="Clear scene",
        default=False,
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self) 
        return {'RUNNING_MODAL'}

    def execute(self, context):
        geometry_path = os.path.join(self.directory, "geometry.bin")
        if not os.path.exists(geometry_path):
            self.report({'ERROR'}, "geometry.bin not found in folder")
            return {'CANCELLED'}
        
        object_path = os.path.join(self.directory, "object.bin")
        if not os.path.exists(object_path):
            self.report({'ERROR'}, "object.bin not found in folder")
            return {'CANCELLED'}

        importModel(self.directory, self.clear_scene)
        return {'FINISHED'}
        
def importModel(directory: str, clear_scene: bool):
    if clear_scene:
        clearScene()

    geometry_path = os.path.join(directory, "geometry.bin")
    geometry_file = open(geometry_path, "rb")
    
    object_path  = os.path.join(directory, "object.bin")
    object_file   = open(object_path, "rb")

    br_geometry = BinaryReader(geometry_file)
    bin_geometry = GEOMETRY()
    bin_geometry.read(br_geometry)

    br_object = BinaryReader(object_file)
    bin_object = OBJECT()
    bin_object.read(br_object)

    folder_name = os.path.basename(os.path.normpath(directory))
    build_bin(bin_geometry, bin_object, folder_name)

    return {'FINISHED'}