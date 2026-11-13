"""Capture scoped native state for the observed post-B172 sailing differences."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B172_repeat_tools_v4395')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/run_lil_B172_display_fixture_v4390.py','scripts/run_lil_B172_repeat_v4395.py',{
        'display_run_v4390':'repeat_run_v4395','display_v4390':'repeat_v4395',
        "\"'--capture-at',*map(str,range(2350,20001,60))\"":"\"'--capture-at','3010','6610','9370','14050','19990'\"",
        "(\"'--dump-capture-ram','--dump-pause-ram','--dump-ram'\", \"'--dump-ram'\")":"(\"'--dump-capture-ram','--dump-pause-ram','--dump-ram'\", \"'--dump-capture-ram','--dump-ram'\")",
        "'fixture_manifest':str(FIXTUREPATH)":"'focused_repeat_for_later_sailing_divergence':True,'post_B172_town_RAM_requested_at9370':True,'fixture_manifest':str(FIXTUREPATH)",
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,
        purpose='Both B172 paths observe27 complete panels and all47 commands;paired whole-RGB town9370 agrees. Two transient nontext differences occur at2950/6730,and98 later sailing samples differ after following B120 exits14133/14136. Test same-ROM reproducibility and scoped persistent state after C200/A000 and before later divergence. Preserve all differences;reuse older causal research only with current exact code-span bindings.',
        frames=20001,captures=[3010,6610,9370,14050,19990],same_ROM_bytes_same_inputs_readonly_original_observer=True,
        no_extra_ROM_build=True,no_new_editorial_or_completion_credit=True,full_goal_complete=False))
    print('Prepared focused B172 repeats with post-effect town9370 and surrounding native-state snapshots.')
