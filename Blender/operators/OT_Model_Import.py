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

class RTUNED_OT_Model_Import(Operator, ImportHelper):
        """Load a R-Tuned Ultimate Street Racing model file"""
        bl_idname = "import_rtuned.data"
        bl_label = "Import R-Tuned Ultimate Street Racing model"

        filename_ext = ""
        filter_glob: StringProperty(default="*", options={'HIDDEN'}, maxlen=255,)

        clear_scene: BoolProperty(
            name="Clear scene",
            description="Clear the scene",
            default=False,
        )

        def execute(self, context):   
            importModel(self.filepath, self.clear_scene)

            return {'FINISHED'}
        
def importModel(filepath: str, clear_scene: bool):
    if clear_scene:
        clearScene()

    file = open(filepath, 'rb')
    filename =  filepath.split("\\")[-1]
    br = BinaryReader(file)

    bin = BIN()
    bin.read(br)
    build_bin(bin, filename)

    return {'FINISHED'}