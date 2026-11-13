"""Prepare focused persistent-state captures for observed later sailing differences."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B171_repeat_tools_v4343')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/run_lil_B171_display_fixture_v4341.py','scripts/run_lil_B171_repeat_v4343.py',{
        'display_run_v4341':'repeat_run_v4343','display_v4341':'repeat_v4343',
        "\"'--capture-at',*map(str,range(2350,20001,60))\"":"\"'--capture-at','3130','7510','11770','16450','19990'\"",
        "(\"'--dump-capture-ram','--dump-pause-ram','--dump-ram'\", \"'--dump-ram'\")":"(\"'--dump-capture-ram','--dump-pause-ram','--dump-ram'\", \"'--dump-capture-ram','--dump-ram'\")",
        "'fixture_manifest':str(FIXTUREPATH)":"'focused_repeat_for_later_sailing_divergence':True,'post_B171_town_RAM_requested_at11770':True,'fixture_manifest':str(FIXTUREPATH)",
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,
        purpose='Both original captures agree throughout B171 and normal town return;59 later sampled upper/name regions differ from16570. Check same-ROM reproducibility and original persistent state before attributing the later difference. Reuse documented scheduler-entropy cause only with byte-exact runtime spans; do not repeat the older causal experiment.',
        frames=20001,captures=[3130,7510,11770,16450,19990],same_ROM_bytes_same_inputs_readonly_original_observer=True,
        no_extra_ROM_build=True,no_new_editorial_or_completion_credit=True,full_goal_complete=False))
    print('Prepared focused B171 repeats with read-only town11770 and surrounding persistent-state snapshots.')
