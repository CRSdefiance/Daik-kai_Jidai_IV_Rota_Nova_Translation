"""Prepare the pending ledger mutation with explicit scoped count changes."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_checkpoint_tools_v4475')
if __name__=='__main__':
    assert not ROOT.exists()
    text=Path('scripts/checkpoint_lil_B173_v4426b.py').read_text(encoding='utf-8')
    note=next(line for line in text.splitlines() if line.startswith('    note = '))
    final=next(line for line in text.splitlines() if line.startswith("    print('V4426 staged"))
    tool=derive('scripts/checkpoint_lil_B173_v4426b.py','scripts/checkpoint_lil_B174_v4475.py',{
        note:"    note = '5833 fresh rereads:5800 integrated/33 pending;source/prose5836. B174 credited once as pending;no completion or actual scene credit.'",
        final:"    print('V4475 staged:5833 reread/5800 integrated/33 pending;5836 source/prose. Promoted V4445 unchanged;full goal active.')",
        'Stage11':'Stage33','lil_B173_checkpoint_v4426':'lil_B174_checkpoint_v4475',
        'editorial_handoff_verification_v4409b/verified_handoff.json':'promotion_v4452/promotion_receipt.json',
        'lil_B173_native_approval_v4425':'lil_B174_native_approval_v4474',
        'lil_B173_editorial_manuscript_v3':'lil_B174_editorial_manuscript_v5',
        'Lil-B173-Reika-crown-inquiry-uncertain-Julian-tomb-lead-competitive-search11':
            'Lil-B174-Julian-Mihwa-crown-gratitude-grandfather-aspiration-conditional-date33',
        'lil_B173_checkpoint_text_v4426':'lil_B174_checkpoint_text_v4475',
        'len(rows) == 11':'len(rows) == 33','(5789,5789,0)':'(5800,5800,0)',
        'len({historical_key(r) for r in selected}) == 11':'len({historical_key(r) for r in selected}) == 33',
        "['/data/SC2.DK4'] == 3936":"['/data/SC2.DK4'] == 3947",
        "['records_with_source_and_prose_pass'] == 5792":"['records_with_source_and_prose_pass'] == 5803",
        '# Current editorial handoff - V4408':'# Current editorial handoff - V4452',
        "['records_with_source_prose_drafts'] = 5803":"['records_with_source_prose_drafts'] = 5836",
        "['/data/SC2.DK4'] = 3947":"['/data/SC2.DK4'] = 3980",
        '3-reviewed-COMMON-incomplete;11-Lil-B173':'3-reviewed-COMMON-incomplete;33-Lil-B174',
        'blocks=[173],records=11':'blocks=[174],records=33',
        'proposed_revisions=8,retentions=3,source_prose_reviews_added=11':'proposed_revisions=23,retentions=10,source_prose_reviews_added=33',
        'fresh_pass_records_explicitly_reread=5800,fresh_pass_records_integrated=5789':'fresh_pass_records_explicitly_reread=5833,fresh_pass_records_integrated=5800',
        'fresh_pass_records_pending_native_actual_release=11':'fresh_pass_records_pending_native_actual_release=33',
        'reviewed_route_records=4201,completed_route_records=4190':'reviewed_route_records=4234,completed_route_records=4201',
        'row_count_notes=5':'row_count_notes=17','all2_speech_sheets_viewed':'all5_speech_sheets_viewed',
        'unfinished_editorial_scope_v4408':'unfinished_editorial_scope_v4449',
        'blocks=[173],count=11':'blocks=[174],count=33','incomplete_route_source_prose_count=11':'incomplete_route_source_prose_count=33',
        'physical_speeches=123':'physical_speeches=90','remaining_B174_B180':'remaining_B175_B180',
        'source_prose_pending_records=11':'source_prose_pending_records=33',
        'incomplete_route_source_prose=11':'incomplete_route_source_prose=33',
        'source_prose_reviews_added=11':'source_prose_reviews_added=33',
        'V4426:11':'V4475:33','new_source_prose_reviews=11':'new_source_prose_reviews=33',
        'proposed_revisions=8,justified_retentions=3':'proposed_revisions=23,justified_retentions=10',
        'fresh_reread=5800,fresh_integrated=5789,fresh_pending=11,source_prose=5803,completed=5789':
            'fresh_reread=5833,fresh_integrated=5800,fresh_pending=33,source_prose=5836,completed=5800',
        'historical_revised=3678,historical_retained=2111':'historical_revised=3686,historical_retained=2114',
        'B173':'B174','v4426':'v4475','V4426':'V4475',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tool=tool,
        explicit_scope_counts_not_global_numeric_substitution=True,no_credit_applied_yet=True,full_goal_complete=False))
    print('Prepared pending B174 checkpoint:33 newly reread, zero new completions; full scope preserved.')
