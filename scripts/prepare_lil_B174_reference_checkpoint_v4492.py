"""Prepare a count-preserving B174 reference/gameplay checkpoint."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_reference_checkpoint_tools_v4492')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/checkpoint_lil_B173_references_v4441.py','scripts/checkpoint_lil_B174_references_v4492.py',{
        'lil_B173_reference_checkpoint_text_v4441':'lil_B174_reference_checkpoint_text_v4492',
        'lil_B173_reference_checkpoint_v4441':'lil_B174_reference_checkpoint_v4492',
        'lil_B173_editorial_manuscript_v3':'lil_B174_editorial_manuscript_v5',
        'lil_B173_editorial_manuscript_v4':'lil_B174_editorial_manuscript_v6',
        'lil_B173_reference_approval_v4440':'lil_B174_reference_approval_v4491',
        'Lil-B173-Reika-crown-inquiry-uncertain-Julian-tomb-lead-competitive-search11':
            'Lil-B174-Julian-Mihwa-crown-gratitude-grandfather-aspiration-conditional-date33',
        'editorial_handoff_verification_v4427':'editorial_handoff_verification_v4480',
        "len(approval['actual_sampled_display_IDs']) == 11 and not approval['offline_only_display_IDs']":
            "len(approval['actual_sampled_display_IDs']) == 32 and approval['offline_only_display_IDs']==['DK4_MES_B174_R0069']",
        '(5800, 5789, 11)':'(5833, 5800, 33)',
        "actual_sampled_display_IDs=approval['actual_sampled_display_IDs'], offline_only_display_IDs=[]":
            "actual_sampled_display_IDs=approval['actual_sampled_display_IDs'], offline_only_display_IDs=approval['offline_only_display_IDs']",
        '5800 rereads/5789 integrated/11 pending;B173':'5833 rereads/5800 integrated/33 pending;B174',
        '3-reviewed-COMMON-incomplete;11-Lil-B173':'3-reviewed-COMMON-incomplete;33-Lil-B174',
        'actual_complete_native_panels=11':'actual_complete_native_panels=32',
        'unfinished_editorial_scope_v4426':'unfinished_editorial_scope_v4475',
        'lil_B173_display_fixture_v4436':'lil_B174_display_fixture_v4487',
        'lil_B173_research_v4431':'lil_B174_research_v4482','assert pinned == 3':'assert pinned == 0',
        'planned = {lp: encode_ledger(ledger), pins_path: encoded(pins)}':'planned = {lp: encode_ledger(ledger)}',
        "'scripts/build_integrated_release.py']":"'scripts/build_integrated_release.py', 'translations/rom_retention_pins.json']",
        'V4441:11 B173':'V4492:33 B174',
        'fresh_reread=5800, integrated=5789, pending=11, source_prose=5803':'fresh_reread=5833, integrated=5800, pending=33, source_prose=5836',
        'reviewed_sheets=2':'reviewed_sheets=6','ROMs_pinned=3':'ROMs_pinned=0, previously_pinned_ROMs_preserved=3',
        'V4441 checkpoint complete:11 reference-approved pending records;11 actual panels/two boots;3 ROMs pinned. MainV4353,registry,builder and all credit counts preserved.':
            'V4492 checkpoint complete:33 reference-approved pending records;32 actual/one offline,two terminal boots;3 prior pins preserved. MainV4445,registry,builder and all counts preserved.',
        'B173':'B174','v4441':'v4492','V4441':'V4492',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tool=tool,
        prior_pins_preserved_without_duplicate_additions=True,actual32_offline1_not_all33_claimed=True,
        no_new_source_prose_orcompletion_credit=True,full_goal_complete=False))
    print('Prepared B174 reference checkpoint,32 actual/one offline, unchanged5833/5800/33 coverage.')
