from ...Utilities import *

from mathutils import *

class GEOMETRY:

    def __init__(self):
        self.__offsets = []
        self.vertex_buffers = []
        self.face_buffers = []

    def read(self, br: BinaryReader):
        buffer_count = br.readUInt()
        unk_size1 = br.readUInt()
        br.seek(unk_size1, 0)
        for _ in range(buffer_count):
            self.__offsets.append(br.readUInt())

        index = 0
        for buffer_offset in self.__offsets:
            print("Reading buffer ", index)
            self.readBuffer(buffer_offset, br)
            index += 1

    def readBuffer(self, offset: int, br: BinaryReader):
        br.seek(offset, 0)
        br.readUInt()
        br.readUInt()
        vertex_count = br.readUInt()

        #offsets
        positions_buffer_offset = br.readUInt() # 12 bytes per count
        normal_buffer_offset = br.readUInt() # 6 bytes per count
        br.seek(8, 1)
        uv1_buffer_offset = br.readUInt() # 8 bytes per count
        uv2_buffer_offset = br.readUInt() # 8 bytes per count
        br.seek(8, 1)
        unk_buffer_offset = br.readUInt() # 8 bytes per count
        br.seek(44, 1)
        br.readUInt()
        faces_count = br.readUInt()
        faces_buffer_offset = br.readUInt()

        vertexBuffer = {
            "positions" : [],
            "colors" : [],
            "normals" : [],
            "texCoords1" : [],
            "texCoords2" : [],
        }

        for _ in range(vertex_count):
            br.seek(positions_buffer_offset + _ * 12)
            vertexBuffer["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])
            br.seek(normal_buffer_offset + _ * 6)
            vertexBuffer["normals"].append(Vector((br.readHalfFloat(), br.readHalfFloat(), br.readHalfFloat())).normalized())
            if uv1_buffer_offset != 0:
                br.seek(uv1_buffer_offset + _ * 8)
                vertexBuffer["texCoords1"].append([br.readFloat(), br.readFloat()])
            if uv2_buffer_offset != 0:
                br.seek(uv2_buffer_offset + _ * 8)
                vertexBuffer["texCoords2"].append([br.readFloat(), br.readFloat()])

        self.vertex_buffers.append(vertexBuffer)

        faceBuffer = []
        br.seek(faces_buffer_offset)
        for _ in range(faces_count):
            faceBuffer.append(br.readUShort())

        self.face_buffers.append(faceBuffer)

        
