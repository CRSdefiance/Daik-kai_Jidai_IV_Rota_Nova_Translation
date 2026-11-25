"""Derive integration-ready coverage and validate complete history before any write."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

root=Path('work/analysis/lil_B176_reference_checkpoint_tools_v4591')
assert not root.exists()
checks="""    previous_ledger=json.loads(before_bytes)
    def same_except(a,b,allowed):
        assert {k:v for k,v in a.items() if k not in allowed}=={k:v for k,v in b.items() if k not in allowed}
    same_except(previous_ledger,ledger,{'contextual_story_natural_dialogue_pass_v1871','active_source_prose_drafts','coverage_units',
        'unfinished_editorial_scope_v4591','lil_B176_reference_reconciliation_v4591','latest_checkpoint'})
    oldfresh=previous_ledger['contextual_story_natural_dialogue_pass_v1871']
    same_except(oldfresh,fresh,{'pending_contextual_families','latest_contextual_manuscript','latest_pending_contextual_family','coverage_note'})
    same_except(oldfresh['pending_contextual_families'][0],pending,{'manuscript','manuscript_sha256','manuscripts','pending',
        'actual_sampled_display_IDs','offline_only_display_IDs','new_emulator_runs','reference_approval','reference_approval_sha256'})
    oldactive=previous_ledger['active_source_prose_drafts']
    same_except(oldactive,active,{'manuscripts','route_record_subsets_pending','status','note'})
    assert active['manuscripts']==oldactive['manuscripts']+[str(DOC)]
    assert active['route_record_subsets_pending']=={**oldactive['route_record_subsets_pending'],str(INPUT):[],str(DOC):[r['id'] for r in doc['records']]}
    for a,b in zip(previous_ledger['coverage_units'],ledger['coverage_units'],strict=True):
        if a['id']==FAMILY:
            same_except(a,b,{'manuscript','manuscript_sha256','manuscripts','pending','actual_sampled_display_IDs','offline_only_display_IDs',
                'new_emulator_runs','reference_approval','reference_approval_sha256','status','actual_new_cold_boot_runs','actual_complete_native_panels','registered_release_pending'})
        elif a['id']=='all-route-scenes':same_except(a,b,{'next'})
        else:assert a==b
    same_except(read(oldscope['path']),inventory,{'next_focus','B176_reference_and_actual_coverage_v4591'})
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert tuple(ledger[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(5865,5878,3728,2137)
    assert len(encode_ledger(ledger))<100*1024*1024
"""
tool=derive('scripts/checkpoint_lil_B175_references_v4537.py','scripts/checkpoint_lil_B176_references_v4591.py',{
    'Record sealed32-actual B175 reference approval':'Record sealed10-actual B176 reference approval',
    'lil_B175_reference_checkpoint_text_v4537':'lil_B176_reference_checkpoint_text_v4591',
    'lil_B175_reference_checkpoint_v4537':'lil_B176_reference_checkpoint_v4591',
    'lil_B175_editorial_manuscript':'lil_B176_editorial_manuscript',
    'lil_B175_reference_approval_v4536':'lil_B176_reference_approval_v4590',
    'Lil-B175-pirate-encirclement-pride-sea-challenge-unnamed-sword-and-banter32':
        'Lil-B176-banana-age-Owner-Cook-doubt-purchase-order-and-prospective-Seville-fashion10',
    'editorial_handoff_verification_v4524/verified_handoff.json':'editorial_handoff_verification_v4578/independent_verified_handoff.json',
    "len(approval['actual_sampled_display_IDs'])==32":"len(approval['actual_sampled_display_IDs'])==10",
    '==(5865,5833,32)':'==(5875,5865,10)',
    '5865 rereads/5833 integrated/32 pending;B175':'5875 rereads/5865 integrated/10 pending;B176',
    '32-Lil-B175-reference-approved':'10-Lil-B176-reference-approved',
    'actual_complete_native_panels=32':'actual_complete_native_panels=10',
    'unfinished_editorial_scope_v4519':'unfinished_editorial_scope_v4573',
    'B175_reference_and_actual_coverage_v4537':'B176_reference_and_actual_coverage_v4591',
    'unfinished_editorial_scope_v4537':'unfinished_editorial_scope_v4591',
    'lil_B175_reference_reconciliation_v4537':'lil_B176_reference_reconciliation_v4591',
    "    pins=read('translations/rom_retention_pins.json')":checks+"    pins=read('translations/rom_retention_pins.json')",
    'lil_B175_display_fixture_v4531/complete_B175_B22_fixtures':'lil_B176_display_fixture_v4585/complete_B176_B22_fixtures',
    'lil_B175_research_v4526':'lil_B176_research_v4580',
    '## V4537:32 B175':'## V4591:10 B176',
    '# Current editorial handoff - V4537':'# Current editorial handoff - V4591',
    "checkpoint='V4537'":"checkpoint='V4591'",'fresh_reread=5865':'fresh_reread=5875',
    'integrated=5833,pending=32,source_prose=5868':'integrated=5865,pending=10,source_prose=5878',
    'reviewed_sheets=6':'reviewed_sheets=2',
    'V4537:32 B175 records':'V4591:10 B176 records','main V4496':'main V4541',
})
root.mkdir(parents=True)
save(root/'source_derivation.json',dict(tool=tool,full_history_semantic_checks_precede_first_metadata_write=True,
    source_prose_or_completion_credit_added=0,full_goal_complete=False))
