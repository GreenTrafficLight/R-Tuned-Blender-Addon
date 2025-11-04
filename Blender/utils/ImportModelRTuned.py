import bpy
import struct
import bmesh
import os

from math import *
from mathutils import *

from ...Utilities import *
from ...Formats.bin import BIN

def build_bin(data: BIN, filename: str):

    bpy.ops.object.add(type="ARMATURE")
    ob = bpy.context.object
    ob.rotation_euler = ( radians(-90), 0, 0 )
    ob.name = str(filename)

    amt = ob.data
    amt.name = str(filename)

    for index in range(len(data.vertex_buffers)):

        if index == 300:
            break

        print("Building mesh ", index)

        empty = add_empty(str(index), ob)

        mesh = bpy.data.meshes.new(str(index))
        obj = bpy.data.objects.new(str(index), mesh)

        empty.users_collection[0].objects.link(obj)

        obj.parent = empty

        vertex_buffer = data.vertex_buffers[index]
        face_buffer = data.face_buffers[index]

        vertexList = {}
        facesList = []
        normals = []

        bm = bmesh.new()
        bm.from_mesh(mesh)

        # Set vertices
        for j in range(len(vertex_buffer["positions"])):
            vertex = bm.verts.new(vertex_buffer["positions"][j])
            
            if vertex_buffer["normals"] != []:
                vertex.normal = vertex_buffer["normals"][j]
                normals.append(vertex_buffer["normals"][j])
            
            vertex.index = j

            vertexList[j] = vertex

        faces = StripToTriangle(face_buffer)     

        # Set faces
        for j in range(0, len(faces)):
            try:
                face = bm.faces.new([vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]])
                face.smooth = True
                facesList.append([face, [vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]]])
            except:
                pass

        # Set uv
        # for f in bm.faces:
        #     uv_layer1 = bm.loops.layers.uv.verify()
        #     for l in f.loops:
        #         l[uv_layer1].uv =  [vertex_buffer["texCoords"][l.vert.index][0], 1 - vertex_buffer["texCoords"][l.vert.index][1]]

        bm.to_mesh(mesh)
        bm.free()