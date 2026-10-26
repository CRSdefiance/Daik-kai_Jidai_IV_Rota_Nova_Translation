"""Focused repeat for later sailing divergence, with read-only post-scene RAM."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B170_repeat_tools_v4295')

if __name__ == '__main__':
    assert not ROOT.exists()
    tool = derive('scripts/run_lil_B170_display_fixture_v4292.py', 'scripts/run_lil_B170_repeat_v4295.py', {
        'display_run_v4292': 'repeat_run_v4295', 'display_v4292': 'repeat_v4295',
        "\"'--capture-at',*map(str,range(2350,20001,60))\"": "\"'--capture-at','3250','8410','11290','16090','19990'\"",
        "(\"'--dump-capture-ram','--dump-pause-ram','--dump-ram'\", \"'--dump-ram'\")": "(\"'--dump-capture-ram','--dump-pause-ram','--dump-ram'\", \"'--dump-capture-ram','--dump-ram'\")",
        "'fixture_manifest':str(FIXTUREPATH)": "'focused_repeat_for_later_sailing_divergence':True,'post_B170_town_RAM_requested_at11290':True,'fixture_manifest':str(FIXTUREPATH)",
    })
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tool=tool,
        purpose='First paired runs agree throughout B170, town return and subsequent B120 command sequence. Later Sea View diverges. Compare original actor/captain models in read-only town-return RAM and compare each ROM repeat with its first run before attributing the difference.',
        frames=20001, captures=[3250, 8410, 11290, 16090, 19990],
        same_ROM_bytes_same_inputs_readonly_original_observer=True, no_extra_ROM_build=True,
        no_new_editorial_or_completion_credit=True, full_goal_complete=False))
