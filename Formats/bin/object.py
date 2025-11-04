from ...Utilities import *

class MODEL_INFORMATION:
    def __init__(self):
        self.meshes_information = []
        self.additional_informations = []

    def deserialize(self, br: BinaryReader):
        br.seek(8, 1) # zeros ?
        br.readBytes(12) # unknown 12 bytes
        meshes_informations_count = br.readUInt()
        meshes_informations_offset = br.readUInt()
        additional_informations_count = br.readUInt()
        additional_informations_offset = br.readUInt() # offset to data structs of size 1200(?) bytes
        
        br.seek(meshes_informations_offset)
        br.seek(4,1)
        for _ in range(meshes_informations_count):
            print("Reading Mesh Information : " + str(_))
            mesh_information = MESH_INFORMATION()
            mesh_information.deserialize(br)
            self.meshes_information.append(mesh_information)

        mesh_information: MESH_INFORMATION
        for mesh_information in self.meshes_information:
            mesh_information.deserialize_submeshes_informations(br)

        br.seek(additional_informations_offset)
        for _ in range(additional_informations_count):
            additional_information = ADDITIONAL_INFORMATION()
            additional_information.deserialize(br)
            self.additional_informations.append(additional_information)

class MESH_INFORMATION:
    # 140 bytes
    def __init__(self):
        self.submeshes_informations_count = 0
        self.submeshes_information_offset = 0
        self.vertex_count = 0
        self.buffer_index = 0
        self.submeshes_informations = []
        self.mesh_name = ""

    def deserialize(self, br: BinaryReader):
        br.seek(4, 1) # zeros ?
        br.readBytes(12) # unknown 12 bytes
        self.submeshes_informations_count = br.readUInt()
        self.submeshes_information_offset = br.readUInt()
        br.readUInt()
        br.readUInt()
        self.vertex_count = br.readUInt()
        self.buffer_index = br.readUInt()
        br.readBytes(32)
        self.mesh_name = br.readBytesToString(68)
        print(br.tell())

    def deserialize_submeshes_informations(self, br: BinaryReader):
        br.seek(self.submeshes_information_offset)
        br.seek(8, 1) # zeros ?
        br.readBytes(12) # unknown 12 bytes

        for _ in range(self.submeshes_informations_count):
            print("Reading Submesh Information : " + str(_))
            submesh_information = SUBMESH_INFORMATION()
            submesh_information.deserialize(br)
            self.submeshes_informations.append(submesh_information)

class SUBMESH_INFORMATION:
    # 92 bytes
    def __init__(self):
        self.material_index = 0
        self.faces_count = 0
        self.face_index_start = 0

    def deserialize(self, br: BinaryReader):
        self.material_index = br.readUInt()
        br.readUInt()
        br.seek(16, 1) # zeros ?
        br.readUInt()
        br.readUInt()
        self.faces_count = br.readUInt()
        br.readUShort()
        br.readUShort()
        self.face_index_start = br.readUInt()
        br.readBytes(48)
        

class ADDITIONAL_INFORMATION:
    # 1200 bytes
    def __init__(self):
        self.material_name = ""

    def deserialize(self, br: BinaryReader):
        br.readBytes(1072)
        self.material_name = br.readBytesToString(64)
        br.readBytes(64)


class OBJECT:
    def __init__(self):
        self.__offsets = []
        self.models_informations = []
        
    def read(self, br: BinaryReader):
        br.readBytes(4)
        model_count = br.readUInt()
        unk_size1 = br.readUInt()
        br.seek(unk_size1)
        for _ in range(model_count):
            self.__offsets.append(br.readUInt())

        for model_offset in self.__offsets:
            print("Reading Model Information")
            br.seek(model_offset)
            br.readUInt()

            model_information = MODEL_INFORMATION()
            model_information.deserialize(br)
            self.models_informations.append(model_information)



