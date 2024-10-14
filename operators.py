import bpy
import os
from bpy_extras.io_utils import ImportHelper
from xml.etree import ElementTree as ET
from .element import (
    ElementTree,
    ListProperty,
    ValueProperty,
)
from .helper_funcs import create_quad, create_materials, quad_min_max, round_to_even


class OT_Import_WaterXML(bpy.types.Operator, ImportHelper):
    bl_idname = "watereditor.open_filebrowser"
    bl_label = "Import water.xml"

    filter_glob: bpy.props.StringProperty(
        default='*.xml;',
    )

    def execute(self, context):

        filename, extension = os.path.splitext(self.filepath)

        folderpath = os.path.dirname(self.filepath)
        filepath = os.path.join(folderpath, (filename+extension))

        dat = WaterData.from_xml_file(filepath)

        print("Starting WaterQuads generation")
        mat = create_materials("WaterQuad", (0, 0.18, 1, 1))
        waterQuadParent = bpy.data.objects.new("WaterQuads", None)
        bpy.context.collection.objects.link(waterQuadParent)
        bpy.context.view_layer.objects.active = waterQuadParent
        count = 1
        for quad in dat.waterQuads:
            verts = [
                (quad.minX, quad.maxY, quad.water_z),
                (quad.minX, quad.minY, quad.water_z),
                (quad.maxX, quad.minY, quad.water_z),
                (quad.maxX, quad.maxY, quad.water_z)
            ]
            faces = [[0, 1, 2, 3]]
            created_quad = create_quad(
                f'WaterQuad{count}', verts, faces, mat, waterQuadParent)
            created_quad.gta_quadtype = 'water'
            created_quad.waterProperties.water_type = quad.water_type
            created_quad.waterProperties.water_is_invisible = quad.is_invisible
            created_quad.waterProperties.water_has_limited_depth = quad.has_limited_depth
            if hasattr(quad, 'has_limited_depth') and quad.has_limited_depth == True:
                created_quad.waterProperties.water_limited_depth = quad.limited_depth
            created_quad.waterProperties.water_z = quad.water_z
            created_quad.waterProperties.water_a1 = quad.a1
            created_quad.waterProperties.water_a2 = quad.a2
            created_quad.waterProperties.water_a3 = quad.a3
            created_quad.waterProperties.water_a4 = quad.a4
            created_quad.waterProperties.water_no_stencil = quad.no_stencil
            count += 1
        print(f"Imported {count} WaterQuads")

        print("Starting CalmingQuads generation")
        mat = create_materials("CalmingQuad", (0, 0.66, 1, 1))
        calmingQuadParent = bpy.data.objects.new("CalmingQuad", None)
        bpy.context.collection.objects.link(calmingQuadParent)
        bpy.context.view_layer.objects.active = calmingQuadParent
        count = 1
        for quad in dat.calmingQuads:
            verts = [
                (quad.minX, quad.maxY, 0),
                (quad.minX, quad.minY, 0),
                (quad.maxX, quad.minY, 0),
                (quad.maxX, quad.maxY, 0)
            ]
            faces = [[0, 1, 2, 3]]
            created_quad = create_quad(
                f'CalmingQuad{count}', verts, faces, mat, calmingQuadParent)
            created_quad.gta_quadtype = 'calming'
            created_quad.waterProperties.water_fDampening = quad.fDampening
            count += 1
        print(f"Imported {count} CalmingQuad")

        print("Starting WaveQuads generation")
        mat = create_materials("WaveQuad", (0, 1, 0.4, 1))
        waveQuadParent = bpy.data.objects.new("WaveQuad", None)
        bpy.context.collection.objects.link(waveQuadParent)
        bpy.context.view_layer.objects.active = waveQuadParent
        count = 1
        for quad in dat.waveQuads:
            verts = [
                (quad.minX, quad.maxY, 0),
                (quad.minX, quad.minY, 0),
                (quad.maxX, quad.minY, 0),
                (quad.maxX, quad.maxY, 0)
            ]
            faces = [[0, 1, 2, 3]]
            created_quad = create_quad(
                f'WaveQuad{count}', verts, faces, mat, waveQuadParent)
            created_quad.gta_quadtype = 'wave'
            created_quad.waterProperties.water_amplitude = quad.amplitude
            created_quad.waterProperties.water_xDirection = quad.x_direction
            created_quad.waterProperties.water_yDirection = quad.y_direction
            count += 1
        print(f"Imported {count} WaveQuads")

        self.report({"INFO"}, "Successfully imported water.xml")
        return {'FINISHED'}


class OT_Export_WaterXML(bpy.types.Operator):
    bl_idname = "watereditor.export_waterxml"
    bl_label = "Export water.xml"

    directory: bpy.props.StringProperty(
        name="Output directory",
        description="Select export output directory",
        subtype="DIR_PATH",
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def get_filepath(self, name):
        return os.path.join(self.directory, name + ".xml")

    def execute(self, context):

        waterxml = WaterData()
        waterQuadsObj = bpy.data.objects['WaterQuads']
        calmingQuadsObj = bpy.data.objects['CalmingQuad']
        waveQuadsObj = bpy.data.objects['WaveQuad']

        waterQuadCount = len(waterQuadsObj.children)
        calmingQuadCount = len(calmingQuadsObj.children)
        waveQuadCount = len(waveQuadsObj.children)

        for object in waterQuadsObj.children:
            waterQuad_xml = create_waterQuad_xml(object)
            waterxml.waterQuads.append(waterQuad_xml)

        for object in calmingQuadsObj.children:
            calmingQuad_xml = create_calmingQuad_xml(object)
            waterxml.calmingQuads.append(calmingQuad_xml)

        for object in waveQuadsObj.children:
            waveQuad_xml = create_waveQuad_xml(object)
            waterxml.waveQuads.append(waveQuad_xml)

        print(
            f"Export {waterQuadCount} WaterQuads, {calmingQuadCount} CalmingQuads, {waveQuadCount} WaveQuads")

        filepath = self.get_filepath("water")
        waterxml.write_xml(filepath)

        self.report({"INFO"}, f"Successfully exported water.xml to {filepath}")
        return {'FINISHED'}


class WaterQuads(ElementTree):
    tag_name = "Item"

    def __init__(self):
        super().__init__()
        self.minX = ValueProperty("minX")
        self.maxX = ValueProperty("maxX")
        self.minY = ValueProperty("minY")
        self.maxY = ValueProperty("maxY")
        self.water_type = ValueProperty("Type")
        self.is_invisible = ValueProperty("IsInvisible")
        self.has_limited_depth = ValueProperty("HasLimitedDepth")
        self.limited_depth = ValueProperty("LimitedDepth")
        self.water_z = ValueProperty("z")
        self.a1 = ValueProperty("a1")
        self.a2 = ValueProperty("a2")
        self.a3 = ValueProperty("a3")
        self.a4 = ValueProperty("a4")
        self.no_stencil = ValueProperty("NoStencil")


class CalmingQuads(ElementTree):
    tag_name = "Item"

    def __init__(self):
        super().__init__()
        self.minX = ValueProperty("minX")
        self.maxX = ValueProperty("maxX")
        self.minY = ValueProperty("minY")
        self.maxY = ValueProperty("maxY")
        self.fDampening = ValueProperty("fDampening")


class WaveQuads(ElementTree):
    tag_name = "Item"

    def __init__(self):
        super().__init__()
        self.minX = ValueProperty("minX")
        self.maxX = ValueProperty("maxX")
        self.minY = ValueProperty("minY")
        self.maxY = ValueProperty("maxY")
        self.amplitude = ValueProperty("Amplitude")
        self.x_direction = ValueProperty("XDirection")
        self.y_direction = ValueProperty("YDirection")


class WaterQuadsProperty(ListProperty):
    list_type = WaterQuads
    tag_name = "WaterQuads"

    @staticmethod
    def from_xml(element: ET.Element):
        new = WaterQuadsProperty()
        for child in element.iter():
            tagName = child.tag
            if tagName == 'Item':
                new.value.append(WaterQuads.from_xml(child))

        return new


class CalmingQuadsProperty(ListProperty):
    list_type = CalmingQuads
    tag_name = "CalmingQuads"

    @staticmethod
    def from_xml(element: ET.Element):
        new = CalmingQuadsProperty()
        for child in element.iter():
            tagName = child.tag
            if tagName == 'Item':
                new.value.append(CalmingQuads.from_xml(child))

        return new


class WaveQuadsProperty(ListProperty):
    list_type = WaveQuads
    tag_name = "WaveQuads"

    @staticmethod
    def from_xml(element: ET.Element):
        new = WaveQuadsProperty()
        for child in element.iter():
            tagName = child.tag
            if tagName == 'Item':
                new.value.append(WaveQuads.from_xml(child))

        return new


class WaterData(ElementTree):
    tag_name = "WaterData"

    def __init__(self):
        super().__init__()
        self.waterQuads = WaterQuadsProperty()
        self.calmingQuads = CalmingQuadsProperty()
        self.waveQuads = WaveQuadsProperty()


def create_waterQuad_xml(object) -> WaterQuads:
    obj_minmax = quad_min_max(object)
    obj_min_xy = obj_minmax[0]
    obj_max_xy = obj_minmax[1]
    quad_object_xml = WaterQuads()
    quad_object_xml.minX = round_to_even(obj_min_xy[0])
    quad_object_xml.maxX = round_to_even(obj_max_xy[0])
    quad_object_xml.minY = round_to_even(obj_min_xy[1])
    quad_object_xml.maxY = round_to_even(obj_max_xy[1])
    quad_object_xml.type = object.waterProperties.water_type

    is_inv_str = str(object.waterProperties.water_is_invisible)
    quad_object_xml.is_invisible = is_inv_str[0].lower() + is_inv_str[1:]

    limited_depth_str = str(object.waterProperties.water_has_limited_depth)
    quad_object_xml.has_limited_depth = limited_depth_str[0].lower(
    ) + limited_depth_str[1:]

    if object.waterProperties.water_has_limited_depth:
        quad_object_xml.limited_depth = object.waterProperties.water_limited_depth
    else:
        if hasattr(quad_object_xml, 'limited_depth'):
            delattr(quad_object_xml, 'limited_depth')
    quad_object_xml.water_z = object.waterProperties.water_z
    quad_object_xml.a1 = object.waterProperties.water_a1
    quad_object_xml.a2 = object.waterProperties.water_a2
    quad_object_xml.a3 = object.waterProperties.water_a3
    quad_object_xml.a4 = object.waterProperties.water_a4

    no_stencil_str = str(object.waterProperties.water_no_stencil)
    quad_object_xml.no_stencil = no_stencil_str[0].lower() + no_stencil_str[1:]
    return quad_object_xml


def create_calmingQuad_xml(object) -> CalmingQuads:
    obj_minmax = quad_min_max(object)
    obj_min_xy = obj_minmax[0]
    obj_max_xy = obj_minmax[1]
    quad_object_xml = CalmingQuads()
    quad_object_xml.minX = round_to_even(obj_min_xy[0])
    quad_object_xml.maxX = round_to_even(obj_max_xy[0])
    quad_object_xml.minY = round_to_even(obj_min_xy[1])
    quad_object_xml.maxY = round_to_even(obj_max_xy[1])
    quad_object_xml.fDampening = object.waterProperties.water_fDampening
    return quad_object_xml


def create_waveQuad_xml(object) -> WaveQuads:
    obj_minmax = quad_min_max(object)
    obj_min_xy = obj_minmax[0]
    obj_max_xy = obj_minmax[1]
    quad_object_xml = WaveQuads()
    quad_object_xml.minX = round_to_even(obj_min_xy[0])
    quad_object_xml.maxX = round_to_even(obj_max_xy[0])
    quad_object_xml.minY = round_to_even(obj_min_xy[1])
    quad_object_xml.maxY = round_to_even(obj_max_xy[1])
    quad_object_xml.amplitude = object.waterProperties.water_amplitude
    quad_object_xml.x_direction = object.waterProperties.water_xDirection
    quad_object_xml.y_direction = object.waterProperties.water_yDirection
    return quad_object_xml
