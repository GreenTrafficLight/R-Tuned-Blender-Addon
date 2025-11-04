from ..Utilities import *


class BIN:

    def __init__(self):
        self.__offsets = []
        self.vertex_buffers = []
        self.face_buffers = []

    def read(self, br: BinaryReader):
        count = br.readUInt()
        unk_size1 = br.readUInt()
        br.seek(unk_size1, 0)
        for _ in range(count):
            self.__offsets.append(br.readUInt())

        index = 0
        for offset in self.__offsets:
            print("Reading mesh ", index)
            self.readMesh(offset, br)
            index += 1

    def readMesh(self, offset: int, br: BinaryReader):
        br.seek(offset, 0)
        br.readUInt()
        br.readUInt()
        vertex_count = br.readUInt()

        #offsets
        positions_buffer_offset = br.readUInt() # 12 bytes per count
        unk_buffer_offset1 = br.readUInt() # 6 bytes per count
        br.seek(8, 1)
        unk_buffer_offset2 = br.readUInt() # 8 bytes per count
        br.seek(12, 1)
        unk_buffer_offset3 = br.readUInt() # 8 bytes per count
        br.seek(44, 1)
        br.readUInt()
        faces_count = br.readUInt()
        faces_buffer_offset = br.readUInt()

        vertexBuffer = {
            "positions" : [],
            "colors" : [],
            "normals" : [],
            "texCoords" : []
        }

        br.seek(positions_buffer_offset, 0)
        for _ in range(vertex_count):
            vertexBuffer["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])

        self.vertex_buffers.append(vertexBuffer)

        faceBuffer = []
        br.seek(faces_buffer_offset, 0)
        for _ in range(faces_count):
            faceBuffer.append(br.readUShort())

        self.face_buffers.append(faceBuffer)

        
