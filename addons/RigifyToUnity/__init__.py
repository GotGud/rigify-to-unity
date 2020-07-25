bl_info = {
    "name": "Rigify to Unity V2",
    "category": "Rigging",
    "description": "Change Rigify rig into Mecanim-ready rig for Unity",
    "location": "At the bottom of Rigify rig data/armature tab",
    "blender":(2,83,0)
}

import bpy

class RigifyToUnity_Panel(bpy.types.Panel):
    bl_label = "Rigify to Unity"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    @classmethod
    def poll(self, context):
        return context.object.type == "ARMATURE" and "DEF-spine.hips" in bpy.context.object.data.bones
    
    def draw(self, context):
        self.layout.operator("rig2unity.humanoid")

        
class RigifyToUnity_Humanoid(bpy.types.Operator):
    bl_idname = "rig2unity.humanoid"
    bl_label = "Convert rig into a Unity Humanoid"
    
    def execute(self, context):
        obj = bpy.context.object
        
        # List of bones included in Unity Humanoid definition.
        uh_bones = {
            "DEF-spine.hips": "Body_Hips",
            "DEF-spine.spine": "Body_Spine",
            "DEF-spine.lower_chest": "Body_Chest",
            "DEF-spine.upper_chest": "Body_UpperChest",
            "DEF-spine.neck": "Head_Neck",
            "DEF-spine.head": "Head_Head",
            # master_eye cannot be reparented! Need to look into how to make eyes.
            # "master_eye.L": "Head_LeftEye",
            # "master_eye.R": "Head_RightEye",
            "DEF-jaw": "Head_Jaw",

            "DEF-shoulder.L": "LeftArm_Shoulder",
            "DEF-upper_arm.L": "LeftArm_Upper",
            "DEF-forearm.L": "LeftArm_Lower",
            "DEF-hand.L": "LeftArm_Hand",

            "DEF-thumb.01.L": "LFingers_Thumb1",
            "DEF-thumb.02.L": "LFingers_Thumb2",
            "DEF-thumb.03.L": "LFingers_Thumb3",
            "DEF-f_index.01.L": "LFingers_Index1",
            "DEF-f_index.02.L": "LFingers_Index2",
            "DEF-f_index.03.L": "LFingers_Index3",
            "DEF-f_middle.01.L": "LFingers_Middle1",
            "DEF-f_middle.02.L": "LFingers_Middle2",
            "DEF-f_middle.03.L": "LFingers_Middle3",
            "DEF-f_ring.01.L": "LFingers_Ring1",
            "DEF-f_ring.02.L": "LFingers_Ring2",
            "DEF-f_ring.03.L": "LFingers_Ring3",
            "DEF-f_pinky.01.L": "LFingers_Little1",
            "DEF-f_pinky.02.L": "LFingers_Little2",
            "DEF-f_pinky.03.L": "LFingers_Little3",

            "DEF-shoulder.R": "RightArm_Shoulder",
            "DEF-upper_arm.R": "RightArm_Upper",
            "DEF-forearm.R": "RightArm_Lower",
            "DEF-hand.R": "RightArm_Hand",

            "DEF-thumb.01.R": "RFingers_Thumb1",
            "DEF-thumb.02.R": "RFingers_Thumb2",
            "DEF-thumb.03.R": "RFingers_Thumb3",
            "DEF-f_index.01.R": "RFingers_Index1",
            "DEF-f_index.02.R": "RFingers_Index2",
            "DEF-f_index.03.R": "RFingers_Index3",
            "DEF-f_middle.01.R": "RFingers_Middle1",
            "DEF-f_middle.02.R": "RFingers_Middle2",
            "DEF-f_middle.03.R": "RFingers_Middle3",
            "DEF-f_ring.01.R": "RFingers_Ring1",
            "DEF-f_ring.02.R": "RFingers_Ring2",
            "DEF-f_ring.03.R": "RFingers_Ring3",
            "DEF-f_pinky.01.R": "RFingers_Little1",
            "DEF-f_pinky.02.R": "RFingers_Little2",
            "DEF-f_pinky.03.R": "RFingers_Little3",

            "DEF-thigh.L": "LeftLeg_Upper",
            "DEF-shin.L": "LeftLeg_Lower",
            "DEF-foot.L": "LeftLeg_Foot",
            "DEF-toe.L": "LeftLeg_Toes",

            "DEF-thigh.R": "RightLeg_Upper",
            "DEF-shin.R": "RightLeg_Lower",
            "DEF-foot.R": "RightLeg_Foot",
            "DEF-toe.R": "RightLeg_Toes"
        }

        bpy.ops.object.mode_set(mode='EDIT')
        
        # Re-organise DEF-bones into a Unity Humanoid hierarchy.
        basic_bones = {
            "DEF-jaw": "DEF-spine.head",
            
            "DEF-shoulder.L": "DEF-spine.upper_chest",
            "DEF-shoulder.R": "DEF-spine.upper_chest",
            "DEF-upper_arm.L": "DEF-shoulder.L",
            "DEF-upper_arm.R": "DEF-shoulder.R",

            "DEF-thigh.L": "DEF-spine.hips",
            "DEF-thigh.R": "DEF-spine.hips"
        }
        for bone, new_parent in basic_bones.items():
            obj.data.edit_bones.get(bone).parent = obj.data.edit_bones.get(new_parent)

        hand_bones = {
            "DEF-hand.L": [
                "DEF-thumb.01.L",
                "DEF-f_index.01.L",
                "DEF-f_middle.01.L",
                "DEF-f_ring.01.L",
                "DEF-f_pinky.01.L"
            ],
            "DEF-hand.R": [
                "DEF-thumb.01.R",
                "DEF-f_index.01.R",
                "DEF-f_middle.01.R",
                "DEF-f_ring.01.R",
                "DEF-f_pinky.01.R"
            ]
        }
        for hand, fingers in hand_bones.items():
            for finger in fingers:
                obj.data.edit_bones.get(finger).parent = obj.data.edit_bones.get(hand)

        # Remove unused DEF-bones.
        for bone in obj.data.edit_bones:
            if bone.name.startswith("DEF-") and bone.name not in uh_bones:
                obj.data.edit_bones.remove(bone)

        bpy.ops.object.mode_set(mode="OBJECT")

        # Renamame bones to match Unity Humanoid.
        for bone, new_name in uh_bones.items():
            obj.pose.bones.get(bone).name = new_name

        self.report({"INFO"}, "Unity ready rig!")                

        return{"FINISHED"}


def register():
    #classes     
    bpy.utils.register_class(RigifyToUnity_Panel)
    bpy.utils.register_class(RigifyToUnity_Humanoid)
    
    
def unregister():
    #classes
    bpy.utils.unregister_class(RigifyToUnity_Panel)
    bpy.utils.unregister_class(RigifyToUnity_Humanoid)
