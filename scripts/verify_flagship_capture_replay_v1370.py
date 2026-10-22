"""Repeat the full actual capture proof on V1364 with native role fallback."""
import inspect
from pathlib import Path
from dk4tool.patch.flagship_capture_precision import current_entries
from scripts.native_flagship_capture_fixture_v1368 import apply_fixture,ROM
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
    old = 'work/analysis/ship_sinking_release_v1343/registered_release_verification.json'
    assert source.count(old)==1
    source = source.replace(old,'work/analysis/flagship_precision_release_v1363/registered_release_verification.json')
    old = "'source_FFFFFFFF_voice1_falls_back_to2011':True"
    assert source.count(old)==1
    source = source.replace(old,old+",'original82478_logical_member16_selected_with_empty_physical_FirstMate_slot':True")
    env = {**previous.__dict__,'__file__':__file__,'ROM':ROM,'apply_fixture':apply_fixture,'current_entries':current_entries,
        'ROOT':Path('work/analysis/flagship_capture_verified_v1370'),
        'RUN':Path('work/analysis/flagship_capture_replay_v1369'),
        'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/flagship_capture_v1369_1364'),
        'GUIDE':Path('E:/Rota Nova translations/Guide screenshots/V1364 Flagship capture')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
