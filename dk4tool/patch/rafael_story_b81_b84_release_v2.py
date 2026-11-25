"""Expose the qualified guarded330-object transaction tothe registered shared extension entry point."""
from dk4tool.patch.rafael_story_b81_b84_release_v1 import plan_release as original

def plan_release(image,baseline,config_path):
    planned,proof=original(image,baseline,config_path)
    return planned,{**proof,'one_complete_NDS_object_commit_after_all_gates':True}
