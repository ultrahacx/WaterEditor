import bpy


class WATEREDITOR_PT_VIEW_PANEL(bpy.types.Panel):
    bl_label = "Water Editor"
    bl_idname = "WATEREDITOR_PT_VIEW_PANEL"
    bl_category = "WaterEditor"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_order = 0

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("watereditor.open_filebrowser")
        row = layout.row()
        row.operator("watereditor.export_waterxml")
        row = layout.row()
        row.label(text="Liked the addon? Consider supporting me")
        row = layout.row()
        url_btn = row.operator('wm.url_open',
                     text='Donate',
                     icon='URL')
        url_btn.url = 'https://ko-fi.com/ultrahacx'


class WATEREDITOR_PT_OBJECT_PANEL(bpy.types.Panel):
    bl_label = "Water Editor"
    bl_idname = "WATEREDITOR_PT_OBJECT_PANEL"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        obj = context.active_object
        row = layout.row()
        row.enabled = False
        if not obj:
            layout.label(
                text="No sollumz objects in scene selected.", icon="ERROR")
        else:
            if obj.gta_quadtype == 'water':
                layout = self.layout
                layout.prop(obj.waterProperties, 'water_type')
                layout.prop(obj.waterProperties, 'water_is_invisible')
                layout.prop(obj.waterProperties, 'water_has_limited_depth')
                if obj.waterProperties.water_has_limited_depth == True:
                    layout.prop(obj.waterProperties, 'water_limited_depth')
                layout.prop(obj.waterProperties, 'water_z')
                layout.prop(obj.waterProperties, 'water_a1')
                layout.prop(obj.waterProperties, 'water_a2')
                layout.prop(obj.waterProperties, 'water_a3')
                layout.prop(obj.waterProperties, 'water_a4')
                layout.prop(obj.waterProperties, 'water_no_stencil')
            elif obj.gta_quadtype == 'calming':
                layout.prop(obj.waterProperties, 'water_fDampening')
            elif obj.gta_quadtype == 'wave':
                layout.prop(obj.waterProperties, 'water_amplitude')
                layout.prop(obj.waterProperties, 'water_xDirection')
                layout.prop(obj.waterProperties, 'water_yDirection')
