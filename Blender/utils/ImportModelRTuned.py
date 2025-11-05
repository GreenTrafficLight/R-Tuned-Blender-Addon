import bpy
import struct
import bmesh
import os
import math

from mathutils import *

from ...Utilities import *
from ...Formats.bin import *

def extract_textures(texture_bin: TextureBin):

    i = 0
    for texture in texture_bin.textures:
        for sub_texture in texture.sub_textures:
            pass
            
        i += 1




def build_bin(geometry: GEOMETRY, object: OBJECT, folder_name: str):

    collection = bpy.data.collections.new(folder_name)
    bpy.context.scene.collection.children.link(collection)
    
    model_information : MODEL_INFORMATION
    for model_information in object.models_informations:
        
        mesh_information : MESH_INFORMATION
        for mesh_information in model_information.meshes_information:
        
            mesh = bpy.data.meshes.new(str(mesh_information.mesh_name))
            obj = bpy.data.objects.new(str(mesh_information.mesh_name), mesh)
            obj.rotation_euler[0] = math.radians(90)

            collection.objects.link(obj)

            vertex_buffer = geometry.vertex_buffers[mesh_information.buffer_index]
            face_buffer = geometry.face_buffers[mesh_information.buffer_index]

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

            submesh_information : SUBMESH_INFORMATION
            index = 0
            for submesh_information in mesh_information.submeshes_informations:

                start = submesh_information.face_index_start // 2
                count = submesh_information.faces_count

                faces = StripToTriangle(face_buffer[start: (start + count)])

                material_information: ADDITIONAL_INFORMATION = model_information.additional_informations[submesh_information.material_index]
                mat_name = material_information.material_name
                mat = bpy.data.materials.get(mat_name)
                if mat is None:
                    mat = bpy.data.materials.new(mat_name)

                if mat.name not in [m.name for m in mesh.materials]:
                    mesh.materials.append(mat)
                mat_index = mesh.materials.find(mat.name)

                # Set faces
                for j in range(0, len(faces)):
                    try:
                        face = bm.faces.new([vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]])
                        face.smooth = True
                        facesList.append([face, [vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]]])
                        face.material_index = mat_index
                    except:
                        pass

                index += 1
            

            # Set uv
            uv_layer1 = bm.loops.layers.uv.get("UVMap1")
            if uv_layer1 is None and vertex_buffer["texCoords1"]:
                uv_layer1 = bm.loops.layers.uv.new("UVMap1")

            uv_layer2 = bm.loops.layers.uv.get("UVMap2")
            if uv_layer2 is None and vertex_buffer["texCoords2"]:
                uv_layer2 = bm.loops.layers.uv.new("UVMap2")

            # assign UVs if layers exist
            for f in bm.faces:
                for l in f.loops:
                    if uv_layer1 and vertex_buffer["texCoords1"]:
                        uv = vertex_buffer["texCoords1"][l.vert.index]
                        l[uv_layer1].uv = (uv[0], 1 - uv[1])
                    if uv_layer2 and vertex_buffer["texCoords2"]:
                        uv = vertex_buffer["texCoords2"][l.vert.index]
                        l[uv_layer2].uv = (uv[0], 1 - uv[1])
                        
            bm.to_mesh(mesh)
            bm.free()
        
