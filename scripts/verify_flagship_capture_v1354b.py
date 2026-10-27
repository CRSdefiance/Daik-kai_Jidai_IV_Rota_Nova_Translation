"""Bind the original logical role1 member selection,not physical assignment.

53D44 calls82478,which chooses existing Gerhard16 even with an empty physical
First Mate slot.82428 is the distinct physical-room getter. Preserve the
predecessor's guard failure and verify the actual source algorithm explicitly.
"""
import inspect
from pathlib import Path
from scripts import verify_flagship_capture_v1354 as previous

if __name__=='__main__':
    source = inspect.getsource(previous.main)
    old = """        actor = get(0x82428,fleets+0x2090,1)
        assert get(0x82478,fleets+0x2090,1)==16 and actor==actors+4+16*32"""
    new = """        identity = get(0x82478,fleets+0x2090,1)
        assert identity==16 and get(0x82428,fleets+0x2090,1)==0
        actor = actors+4+identity*32
        assert get(0x7EE08,actor)==16
        assert arm[0x82428:0x82570]==clean[0x82428:0x82570]"""
    assert source.count(old)==1
    source = source.replace(old,new)
    old = "'source_FFFFFFFF_voice1_falls_back_to2011':True"
    new = old+",'source53D44_uses82478_logical_member16_with_empty_physical_FirstMate_slot':True"
    assert source.count(old)==1
    source = source.replace(old,new)
    old = "'no_ship_sinking_or_other_new_translation_completion_claim':True"
    new = old+",'predecessor_physical_role_object_assumption_corrected_from_original53D44_82478_code':True"
    assert source.count(old)==1
    source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/flagship_capture_verified_v1354b')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
