"""Independently verify B181's ten uncredited native and stored-review objects."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read

def audit_native(entry):
    from scripts.prepare_lil_B181_checkpoint_v4849b import EVIDENCE
    for p in EVIDENCE:assert entry['evidence'][str(Path(p))]==sha(Path(p).read_bytes())
    doc=read(entry['manuscript']);font=read(doc['native_font_proof']);plan,stored,names,terms=map(read,EVIDENCE)
    assert len(doc['records'])==10 and doc['revised']==doc['retained']==5
    assert entry['approved_uncredited_objects']==10 and entry['source_prose_or_completion_credit_added']==0
    assert entry['relocation_and_stored_checks_complete'] and entry['new_ROMs']==entry['new_emulator_runs']==0
    assert len(font['cases'])==10 and font['current_original_macro_alignment_calls']==80
    assert font['complete_progressive_planes']==9 and font['complete_FE_logical_and_physical_planes']==1
    assert len(font['negative_controls'])==20 and all(r['rejected'] for r in font['negative_controls'])
    assert doc['all10_current_native_previews_viewed_on_two_sheets']
    approval=read('work/analysis/lil_B181_native_approval_v4845/all10_source_prose_current_native_approval.json')
    assert len(approval['formatter_negatives'])==28
    for s in approval['reviewed_sheets']:assert s['viewed_in_full_current_turn'] and sha(Path(s['path']).read_bytes())==s['sha256']
    b=plan['blocks'][0];assert b['block']==181 and len(b['command_map'])==13 and len(b['text_records'])==10
    assert b['source_bytes']==b['source_logical_end']==396 and b['research_bytes']==b['research_logical_end']==380
    assert not b['relative_skip_fixups'] and not b['target_native_skip_cases']
    assert b['original_declared_end_word_maps']==[dict(source_offset=392,target_offset=376,extent=4,source_four_zero_bytes_exact=True)]
    assert b['inverse_restoration_recovers_every_original_logical_byte']
    assert stored['current_final_stored_macro_alignment_cases']==40 and stored['all10_final_targets_complete_native_planes_equal_reviewed_planes']
    assert stored['new_parity_macro_alignment_cases']==12 and stored['exact_byte_identical_reused_macro_alignment_cases']==28
    assert len(names['native_six_consumer_cases']['rows'])==6
    assert terms['city']=='Athens' and terms['commodity']=='Rubies' and terms['commodity_index']==73
    assert terms['old_Japanese_Athens_storage_not_mistaken_for_untranslated_live_alias']
    alias=next(r for r in terms['two_source_current_city_aliases'] if r['pointer_field']==0x1223A4)
    assert alias['current_runtime_pointer']==0x02387FEC and alias['current_exact_deployed_payload_offset']==0x5CC
    assert [r['english'].split('}',1)[1] for r in doc['records'] if r['source_record_index'] in [27,31,35]]==['Quite so. Ahh...','Ahh...','Ahh...']
