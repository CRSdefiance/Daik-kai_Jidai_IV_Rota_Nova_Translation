"""Bind all three exact source/current/research-final records;no actual orformatting approval added."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B50_final_refs_v8498')
OLD=Path('translations/hodram_B50_editorial_manuscript_v2.json')
DOC=Path('translations/hodram_B50_editorial_manuscript_v3.json')
MAP=Path('work/analysis/Hodram_B50_relocation_v8495/reconstruction.json')
STORED=Path('work/analysis/Hodram_B50_stored_v8496/stored_bodies.json')
CONTROLS=Path('work/analysis/Hodram_B50_controls_v8497/stored_controls.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();old,mapping,stored,controls=map(read,[OLD,MAP,STORED,CONTROLS]);group=mapping['groups'][0];raw=Path(group['target_block']).read_bytes()
    assert mapping['manuscript_sha256']==stored['manuscript_sha256']==sha(OLD.read_bytes()) and stored['relocation_sha256']==controls['relocation_sha256']==sha(MAP.read_bytes())
    assert stored['all3_ink_planes_exact_to_already_viewed'] and controls['all3_source_actors_voices_full_preambles_stored_bodies_andoriginal_null_FE_exact']
    assert controls['no_relative_orquery_sites_and25_normal_value_carries_pass'] and len(controls['relocated_picture_andhide_boundary_cases'])==2
    rows=[];changes=[]
    for original,ref in zip(old['records'],mapping['records'],strict=True):
        assert original['id']==ref['id'];row=deepcopy(original);at=ref['final_reference']['offset'];value=bytes.fromhex(ref['stored_hex'])
        assert raw[at:at+len(value)+1]==value+b'\0' and sha(raw)==ref['final_reference']['target_block_sha256']
        assert original['source_reference']==ref['source_reference'] and original['current_reference']==ref['current_reference'] and original['compiled_hex']==ref['compiled_hex']
        changes.append(dict(id=row['id'],previous_current_English_dialogue_still_unconsulted=row.get('current_English_dialogue_still_unconsulted'),current_English_dialogue_still_unconsulted=False,reason='The preserved clean firstgloss wasunconsulted;current English wasexposed onlyafter source/native view andthen reviewed in8488-8489. Original gloss remainsimmutable.'))
        row.update(final_reference=deepcopy(ref['final_reference']),final_hex=ref['stored_hex'],stored_hex=ref['stored_hex'],compiler_owned_parity_space=ref['parity_space_added'],current_English_dialogue_still_unconsulted=False,source_meaning_only_not_localized_orformatting_approval=False,registered_integration_pending=True,formatting_approval_pending_actual_transition_policy_andrelease=True,current_review_status='source-context-prose-native-stored-controls-reviewed-actual-policy-atomic-registered-pending')
        assert row['english']==original['english'] and row['review']==original['review'] and row['review']['formatting'] is False;rows.append(row)
    commands=group['all_target_commands'];FE=next(c for c in commands if c['word']==0x4000 and c['whole_command_hex'][10:12]=='fe');clear=next(c for c in commands if c['word']==0x6302)
    assert FE['offset']==106 and clear['offset']==154 and FE['offset']<clear['offset']
    source=read('work/analysis/Hodram_B50_clean_v8482/complete_clean_SC1_B50_EV1_andcoverage_before_current_English.json')['groups'][0]['commands'];assert next(c for c in source if c['word']==0x6302)['offset']==204
    previous=read('work/analysis/Hodram_B49_relocation_v8398/reconstruction.json')['groups'][0]['all_target_commands'];previousFE=next(c for c in previous if c['word']==0x4000 and c['whole_command_hex'][10:12]=='fe');previousclear=next(c for c in previous if c['word']==0x6302);assert previousclear['offset']<previousFE['offset']
    risk=dict(id='B50_FE_before_6302_distinct_original_transition',source_FE_header_offset=162,source_6302_offset=204,target_FE_header_offset=FE['offset'],target_6302_offset=clear['offset'],all_original_order_preserved=True,preceding_B49_FE_follows_6302=True,actual_source_andEnglish_FE_header_portrait_typed_view_palette_VRAM_anditem_transition_need_representative_capture=True,do_not_assume_B49_absent_FE_header_behavior_for_B50=True,no_control_move_engine_fix_ornew_personal_FE_actor_authorized=True)
    ROOT.mkdir(parents=True);doc=deepcopy(old);doc.update(records=rows,predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),compiled_prose_manuscript='translations/hodram_B50_editorial_manuscript_v1.json',compiled_prose_manuscript_sha256=read('work/analysis/Hodram_B50_pages_v8492b/compiled_native_pages.json')['manuscript_sha256'],source_current_final_references_complete=True,reference_scope='Exact proposed research block/archive;no registered B50 ROM oractual scene yet.',reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),stored_native_proof=str(STORED),stored_native_proof_sha256=sha(STORED.read_bytes()),stored_control_proof=str(CONTROLS),stored_control_proof_sha256=sha(CONTROLS.read_bytes()),distinct_actual_transition_risk=risk,all_three_formatting_gates_still_false=True,status='source-context-prose-native-stored-controls-reviewed-actual-policy-atomic-registered-pending')
    save(DOC,doc);save(ROOT/'reference_binding.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),predecessor=str(OLD),predecessor_sha256=sha(OLD.read_bytes()),all3_exact_source_current_research_final_refs_bound=True,records=mapping['records'],metadata_status_corrections=changes,approved_words_all_source_current_compiled_stored_bytes_andreview_gates_unchanged=True,distinct_actual_transition_risk=risk,all_three_formatting_gates_false=True,no_ROM_registration_actual_scene_orcredit=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [OLD,MAP,STORED,CONTROLS,Path(__file__)]}))
    print('B50all3source-current-researchfinalrefs bound. OriginalFE precedes6302(unlikeB49);actualheader/portrait/palette/itemtransition remainsfocusedrisk. Sourcefirstflags madehistorical;words/bytes/gates unchanged.NoROM orcredit.')
