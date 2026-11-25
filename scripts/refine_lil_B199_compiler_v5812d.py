"""Require each actual panel/hold,not just a trusted coverage-count summary."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B199_compiler_coverage_guards_v5812d')
if __name__=='__main__':
    assert not ROOT.exists()
    needle="    require([len(v['command_pairs']) for v in actual['versions']]==[56,56]"
    extra='''    require(len(actual['actual_panels'])==31 and [p['id'] for p in actual['actual_panels']]==mapping['actual_sampled_display_IDs']
        and sum(len(p['holds']) for p in actual['actual_panels'])==120,'individual actual panels/holds required')
    for panel,row in zip(actual['actual_panels'],doc['records'],strict=True):
        require(panel['id']==row['id'] and panel['prefix']==row['source_selector'] and panel['holds']
            and panel['native_plane_sha256']==row['native_font_case']['whole_native_plane_sha256'],'actual panel identity/native plane differs')
        for hold in panel['holds']:
            require(hold['complete_ink_gray_masks_equal_native_plane'] and hold['upper_portrait_name_and_item_regions_equal_source']
                and sha(Path(hold['capture']).read_bytes())==hold['capture_sha256']
                and sha(Path(hold['clean_capture']).read_bytes())==hold['clean_capture_sha256'],'complete source-paired actual capture required')
'''
    tool=derive('dk4tool/patch/lil_B199_editorial_v1.py','dk4tool/patch/lil_B199_editorial_v2.py',{needle:extra+needle})
    test=derive('scripts/validate_lil_B199_atomic_v5813.py','scripts/validate_lil_B199_atomic_v5813b.py',{
        'lil_B199_editorial_v1':'lil_B199_editorial_v2','lil_B199_atomic_v5813':'lil_B199_atomic_v5813b'})
    ROOT.mkdir(parents=True);save(ROOT/'individual_actual_panel_and_hold_guards.json',dict(tool=tool,test=test,
        synthetic_missing_actual_panel_caught_before_registration=True,no_live_ROM_or_translation_change=True,
        every31_actual_ID_prefix_plane_and120_source_paired_holds_required=True,full_goal_complete=False))
