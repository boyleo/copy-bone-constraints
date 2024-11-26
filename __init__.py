bl_info = {
    "name": "Copy Bone Constraints",
    "blender": (4, 2, 0),
    "category": "Object",
    "version": (1, 0),
    "author": "Boonsak Watanavisit",
    "description": "Copy bone constraints from a source armature to a target armature with matching bone names.",
}

import bpy

class CopyBoneConstraintsPanel(bpy.types.Panel):
    bl_label = "Copy Bone Constraints"
    bl_idname = "OBJECT_PT_copy_bone_constraints"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "source_armature", text="Source Armature")
        layout.prop(scene, "target_armature", text="Target Armature")
        layout.prop(scene, "remove_constraints_from_target_bones_first")
        
        # Indent the second option to indicate it's a subset of the first
        row = layout.row()
        row.enabled = scene.remove_constraints_from_target_bones_first
        row.prop(scene, "remove_constraints_from_all_bones")
        
        layout.prop(scene, "filter_by_prefix")
        layout.prop(scene, "filter_by_suffix")
        
        layout.operator("object.copy_bone_constraints_operator")

class CopyBoneConstraintsOperator(bpy.types.Operator):
    bl_idname = "object.copy_bone_constraints_operator"
    bl_label = "Copy Bone Constraints"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        source_armature_name = scene.source_armature
        target_armature_name = scene.target_armature
        remove_constraints_from_target_bones_first = scene.remove_constraints_from_target_bones_first
        remove_constraints_from_all_bones = scene.remove_constraints_from_all_bones
        filter_by_prefix = scene.filter_by_prefix
        filter_by_suffix = scene.filter_by_suffix

        if not source_armature_name or not target_armature_name:
            self.report({'ERROR'}, "Please select both source and target armatures.")
            return {'CANCELLED'}

        source_armature = bpy.data.objects.get(source_armature_name)
        target_armature = bpy.data.objects.get(target_armature_name)

        if not source_armature or not target_armature:
            self.report({'ERROR'}, "Selected armatures not found.")
            return {'CANCELLED'}

        bpy.context.view_layer.objects.active = source_armature
        bpy.ops.object.mode_set(mode='POSE')

        bpy.context.view_layer.objects.active = target_armature
        bpy.ops.object.mode_set(mode='POSE')

        if remove_constraints_from_all_bones:
            for bone in target_armature.pose.bones:
                for constraint in bone.constraints:
                    bone.constraints.remove(constraint)

        if remove_constraints_from_target_bones_first or remove_constraints_from_all_bones:
            for source_bone in source_armature.pose.bones:
                if filter_by_prefix and not source_bone.name.startswith(filter_by_prefix):
                    continue
                if filter_by_suffix and not source_bone.name.endswith(filter_by_suffix):
                    continue

                target_bone = target_armature.pose.bones.get(source_bone.name)

                if target_bone:
                    for constraint in target_bone.constraints:
                        target_bone.constraints.remove(constraint)

                    for constraint in source_bone.constraints:
                        new_constraint = target_bone.constraints.copy(constraint)
                        new_constraint.name = constraint.name
        else:
            for source_bone in source_armature.pose.bones:
                if filter_by_prefix and not source_bone.name.startswith(filter_by_prefix):
                    continue
                if filter_by_suffix and not source_bone.name.endswith(filter_by_suffix):
                    continue

                target_bone = target_armature.pose.bones.get(source_bone.name)

                if target_bone:
                    for constraint in source_bone.constraints:
                        new_constraint = target_bone.constraints.copy(constraint)
                        new_constraint.name = constraint.name

        self.report({'INFO'}, "Constraints copied successfully.")
        return {'FINISHED'}

def armature_filter(self, object):
    return object.type == 'ARMATURE'

def register():
    bpy.utils.register_class(CopyBoneConstraintsPanel)
    bpy.utils.register_class(CopyBoneConstraintsOperator)
    bpy.types.Scene.source_armature = bpy.props.PointerProperty(type=bpy.types.Object, name="Source Armature", description="Select the source armature", poll=armature_filter)
    bpy.types.Scene.target_armature = bpy.props.PointerProperty(type=bpy.types.Object, name="Target Armature", description="Select the target armature", poll=armature_filter)
    bpy.types.Scene.remove_constraints_from_target_bones_first = bpy.props.BoolProperty(name="Remove Constraints from Target Bones First", description="Remove constraints from matching bones in the target armature before copying new ones", default=True)
    bpy.types.Scene.remove_constraints_from_all_bones = bpy.props.BoolProperty(name="Remove Constraints from All Bones", description="Remove constraints from all bones in the target armature before copying", default=False)
    bpy.types.Scene.filter_by_prefix = bpy.props.StringProperty(name="Prefix", description="Filter bones by prefix in their names")
    bpy.types.Scene.filter_by_suffix = bpy.props.StringProperty(name="Suffix", description="Filter bones by suffix in their names")

def unregister():
    bpy.utils.unregister_class(CopyBoneConstraintsPanel)
    bpy.utils.unregister_class(CopyBoneConstraintsOperator)
    del bpy.types.Scene.source_armature
    del bpy.types.Scene.target_armature
    del bpy.types.Scene.remove_constraints_from_target_bones_first
    del bpy.types.Scene.remove_constraints_from_all_bones
    del bpy.types.Scene.filter_by_prefix
    del bpy.types.Scene.filter_by_suffix

if __name__ == "__main__":
    register()