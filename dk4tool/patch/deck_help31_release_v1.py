"""Exclusive registered owner for30 Deck articles andthe zero-credit Coerce amendment."""
from dk4tool.patch.reviewed_remaining_help_release_v1 import plan_release as original,require,load

def plan_release(image,baseline,config_path):
    require(load(config_path)['kind']=='deck31','exclusive Deck31 owner')
    planned,proof=original(image,baseline,config_path)
    return planned,{**proof,'one_complete_NDS_object_commit_after_all_gates':True}
