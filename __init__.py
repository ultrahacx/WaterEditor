import bpy
from .ui import WATEREDITOR_PT_VIEW_PANEL, WATEREDITOR_PT_OBJECT_PANEL
from .operators import OT_Import_WaterXML, OT_Export_WaterXML

bl_info = {
    "name": "WaterEditor",
    "author": "ultrahacx",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > N",
    "description": "Modify GTAV water.xml",
    "doc_url": "https://github.com/ultrahacx/WaterEditor"
}


class WaterProperties(bpy.types.PropertyGroup):
    water_type: bpy.props.IntProperty(name="Water Type")
    water_is_invisible: bpy.props.BoolProperty(name="Is Invisible")
    water_has_limited_depth: bpy.props.BoolProperty(name="Has Limited Depth")
    water_limited_depth: bpy.props.FloatProperty(name="Limited Depth")
    water_z: bpy.props.FloatProperty(name="Water Z")
    water_a1: bpy.props.IntProperty(name="A1")
    water_a2: bpy.props.IntProperty(name="A2")
    water_a3: bpy.props.IntProperty(name="A3")
    water_a4: bpy.props.IntProperty(name="A4")
    water_no_stencil: bpy.props.BoolProperty(name="No Stencil")
    water_fDampening: bpy.props.FloatProperty(name="Dampening")
    water_amplitude: bpy.props.FloatProperty(name="Amplitude")
    water_xDirection: bpy.props.FloatProperty(name="xDirection")
    water_yDirection: bpy.props.FloatProperty(name="yDirection")


def register():
    bpy.types.Object.gta_quadtype = bpy.props.StringProperty()

    bpy.utils.register_class(OT_Import_WaterXML)
    bpy.utils.register_class(OT_Export_WaterXML)
    bpy.utils.register_class(WaterProperties)

    bpy.types.Object.waterProperties = bpy.props.PointerProperty(
        type=WaterProperties)

    bpy.utils.register_class(WATEREDITOR_PT_VIEW_PANEL)
    bpy.utils.register_class(WATEREDITOR_PT_OBJECT_PANEL)


def unregister():
    del bpy.types.Object.gta_quadtype
    del bpy.types.Object.waterProperties

    bpy.utils.unregister_class(OT_Import_WaterXML)
    bpy.utils.unregister_class(OT_Export_WaterXML)

    bpy.utils.unregister_class(WATEREDITOR_PT_VIEW_PANEL)
    bpy.utils.unregister_class(WATEREDITOR_PT_OBJECT_PANEL)
