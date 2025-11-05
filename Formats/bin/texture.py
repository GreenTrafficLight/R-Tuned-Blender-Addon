from ...Utilities import *

from enum import IntEnum

class TextureFormat(IntEnum):
    Unknown = -1
    A8 = 0
    RGB8 = 1
    RGBA8 = 2
    RGB5 = 3
    RGB5A1 = 4
    RGBA4 = 5
    DXT1 = 6
    DXT1a = 7
    DXT3 = 8
    DXT5 = 9
    ATI1 = 10
    ATI2 = 11
    L8 = 12
    L8A8 = 13

class TextureBin:
    def __init__(self):
        self.textures: list[Texture] = []

    def deserialize(self, br: BinaryReader):
        save_pos = br.tell()
        signature = br.readBytesToString(4)

        texture_count = br.readUInt()
        info = br.readUInt()

        for _ in range(texture_count):
            offset = br.readUInt()
            br.seek(save_pos + offset)
            texture = Texture()
            texture.deserialize(br)
            self.textures.append(texture)
            br.seek(save_pos + 12 + _ * texture_count)

class Texture:
    def __init__(self):
        self.sub_textures: list[SubTexture] = []

    def deserialize(self, br: BinaryReader):
        save_pos = br.tell()
        signature = br.readBytesToString(4)

        sub_texture_count = br.readUInt()
        info = br.readUInt()

        mipMap_count = info & 0xFF
        array_size = (info >> 8) & 0xFF

        if array_size == 1 and mipMap_count != sub_texture_count:
            mipMap_count = sub_texture_count

        self.sub_textures = [[None] * mipMap_count for _ in range(array_size)]

        for i in range(array_size):
            for j in range(mipMap_count):
                offset = br.readUInt()
                br.seek(save_pos + offset)
                sub_texture = SubTexture()
                sub_texture.deserialize(br)
                self.sub_textures[i][j] = sub_texture
                br.seek(save_pos + 12 + _ * mipMap_count)

class SubTexture:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.format: TextureFormat = TextureFormat.A8
        self.data = None 

    def deserialize(self, br: BinaryReader):
        signature = br.readBytesToString(4)

        self.width = br.readUInt()
        self.height = br.readUInt()
        self.format = TextureFormat(br.readUInt())
        br.seek(4, 1)

        data_size = br.readUInt()
        self.data = br.readBytes(data_size)