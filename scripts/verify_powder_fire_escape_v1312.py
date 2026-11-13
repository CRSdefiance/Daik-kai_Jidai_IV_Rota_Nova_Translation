"""Preserve13 escape pipelines using a snapshot from the actual source ROM cohort."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_escape_v1262 as previous
from scripts.verify_village_wrap_v608 import read

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    old = 'work/analysis/battle_aftermath_payload_v1259/native_payload_plan.json'
    assert source.count(old) == 1
    source = source.replace(old,'work/analysis/powder_fire_payload_v1309/native_payload_plan.json')
    old = "context = read('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json')"
    assert source.count(old) == 1
    binding = read('work/analysis/powder_fire_context_v1303c/source_and_actual_binding.json')
    source = source.replace(old,"context = "+repr({'snapshot':'E:/Rota Nova translations/Generated/work/emulation_v193/town_gunnery_v1300_1266/frame_007210_arm9_ram.bin',
        'snapshot_sha256':binding['actual_old_wording_holds'][0]['RAM_sha256']}))
    env = {**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/powder_fire_escape_v1312')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
