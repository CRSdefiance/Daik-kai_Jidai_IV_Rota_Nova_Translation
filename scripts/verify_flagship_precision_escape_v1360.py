"""Preserve thirteen original escape pipelines on the exact source V1344 RAM."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_escape_v1262 as previous
from scripts.verify_village_wrap_v608 import read

if __name__=='__main__':
    source = inspect.getsource(previous.main)
    old = 'work/analysis/battle_aftermath_payload_v1259/native_payload_plan.json'
    assert source.count(old)==1
    source = source.replace(old,'work/analysis/flagship_precision_payload_v1356/native_payload_plan.json')
    old = "context = read('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json')"
    actual = read('work/analysis/flagship_capture_verified_v1354b/actual_flagship_capture_verification.json')
    context = {'snapshot':'E:/Rota Nova translations/Generated/work/emulation_v193/ship_sinking_v1353_1344/frame_010800_arm9_ram.bin',
        'snapshot_sha256':actual['complete_actual2011_holds'][0]['RAM_sha256']}
    assert source.count(old)==1
    source = source.replace(old,'context = '+repr(context))
    env = {**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/flagship_precision_escape_v1360')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
