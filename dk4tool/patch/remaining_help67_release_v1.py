"""Exclusive registered owner forthe67 remaining source Help articles."""
from dk4tool.patch.reviewed_remaining_help_release_v1 import plan_release as original,require,load

def plan_release(image,baseline,config_path):
    require(load(config_path)['kind']=='remaining67','exclusive remaining67 owner')
    planned,proof=original(image,baseline,config_path)
    return planned,{**proof,'one_complete_NDS_object_commit_after_all_gates':True}
