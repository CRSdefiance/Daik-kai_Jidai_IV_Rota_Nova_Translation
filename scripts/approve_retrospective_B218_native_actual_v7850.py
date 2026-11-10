"""Approve the complete retrospective layout after native, actual, inverse and policy checks."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.lil_B218_retrospective_profile_v1 import contract,profile_for
from dk4tool.dialogue.lil_B218_retrospective_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_approval_v7850')
OLD=Path('translations/lil_B218_retrospective_layout_manuscript_v1.json')
NEW=Path('translations/lil_B218_retrospective_layout_manuscript_v2.json')
MAP=Path('work/analysis/retrospective_B218_relocation_v7839b/all13_bound_one_changed_wrap15_commands_complete_clean_predecessor_inverse.json')
ACTUAL=Path('work/analysis/retrospective_B218_actual_v7846/two_English_scenes_complete_masks_commands_andall_measured_late_limits.json')
VIEW=Path('work/analysis/retrospective_B218_actual_view_v7847/26_actual_panes_eight_sheets_andall_measured_limits_viewed.json')
POLICY=Path('work/analysis/retrospective_B218_policy_validation_v7849/13_positives221_actual_changing_policy_rejections.json')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    doc,mapping,actual,view,policy=map(read,[OLD,MAP,ACTUAL,VIEW,POLICY]);c=contract()
    assert mapping['manuscript_sha256']==policy['manuscript_sha256']==sha(OLD.read_bytes())
    assert view['actual_proof_sha256']==sha(ACTUAL.read_bytes()) and view['all_eight_sheets_directly_viewed']
    assert policy['positive_count']==13 and policy['negative_count']==221 and policy['all_negative_inputs_actually_changed_andrejected']
    assert mapping['complete_clean_andpredecessor_blocks_inverse_exact'] and mapping['full_predecessor_archive_inverse_exact']
    assert actual['total_actual_pages']==26 and actual['total_actual_complete_body_andheader_holds']==102 and not actual['total_incomplete_sampled_holds']
    assert actual['all24_original_command_results_andUI_equal'] and actual['both_jobs_terminal_andreaped']
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[218]
    panels={p['id']:p for p in next(g for g in actual['groups'] if g['case']=='proposed_English')['panels']}
    for i,oldrow in enumerate(doc['records']):
        ident=oldrow['id'];row=deepcopy(next(r for r in mapping['records'] if r['id']==ident));b=c['record_bindings'][ident]
        profile=profile_for(arm,block,ident);encoded=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile)
        report=audit_relocatable_dialogue_record(bytes.fromhex(row['source_hex']),row['english'],profile)
        assert encoded.encoded.hex()==b['compiled_hex']==row['proposed_compiled_hex']
        assert all(oldrow['review'][k] for k in ['source','context','localization','naturalness'])
        row.update(compiled_hex=encoded.encoded.hex(),formatted_markup=encoded.formatted_markup,
            base_QA_report=report,qa_waivers=[],qa_waiver_reason=None,row_count_reason=b['row_count_reason'],
            reviewed_ordinary_boundaries=b['ordinary_wrap_reasons'],native_page_count=1,
            actual_record_observed=True,actual_complete_body_andheader_holds=len(panels[ident]['complete_body_andheader_holds']),
            retrospective_all13_wordings_retained=True,no_new_source_prose_orcompletion_credit=True,
            proposed_changed_native_storage_actual_policy_andregistered_release_pending=False,
            registered_integration_pending=True,
            formatting_reason='Complete source/current exchange reread;one automatic predicate wrap changed and12 stored plans retained exactly. Changed logical/compiled/stored native characters,planes,bounds,guards andconsumption pass;both actual13-speech scenes/all24 original commands and102 complete body/name holds are bound;all26 panes/eight sheets viewed;13 positive/221 actual-changing policy cases pass. All controls/inverses andmeasured differences remain. Atomic registered release still pending.')
        row['review']=dict(source=True,context=True,localization=True,naturalness=True,formatting=True)
        doc['records'][i]=row
    assert len(doc['records'])==13 and all(all(r['review'].values()) for r in doc['records'])
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),encoder='dialogue-relocatable-v1',
        native_contract='translations/lil_B218_retrospective_native_contract_v1.json',
        native_contract_sha256=sha(Path('translations/lil_B218_retrospective_native_contract_v1.json').read_bytes()),
        proposed_formatting_native_storage_actual_policy_release_pending=False,
        formatting_review_pending=False,all13_five_individual_gates_approved=True,
        source_current_relocation_proof=str(MAP),source_current_relocation_proof_sha256=sha(MAP.read_bytes()),
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        actual_view=str(VIEW),actual_view_sha256=sha(VIEW.read_bytes()),
        policy_validation=str(POLICY),policy_validation_sha256=sha(POLICY.read_bytes()),
        atomic_registered_release_andmetadata_completion_pending=True,
        actual_pages=26,actual_complete_body_andheader_holds=102,
        actual_capture_scope='Two fresh previous/proposed English initialized scenes,16001 frames each;no new Japanese capture or natural optional activation.',
        all_measured_limits_andfull207_name_review_preserved=True,
        source_prose_andcompletion_credit_added=0,new_credit=0,new_emulator_runs=0,
        full_goal_complete=False)
    ROOT.mkdir(parents=True);save(NEW,doc)
    save(ROOT/'all13_five_gates_approved_one_wrap_no_duplicate_credit.json',dict(manuscript=str(NEW),manuscript_sha256=sha(NEW.read_bytes()),
        all13_individual_five_gates_approved=True,all13_wordings_retained_one_automatic_wrap_changed=True,
        original15_commands13_preambles_zero_macros_andboth_inverses_preserved=True,
        all_measured_timing_RGB_component_actor_seed_limits_preserved=True,
        new_credit=0,atomic_registered_release_andmetadata_completion_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [OLD,MAP,ACTUAL,VIEW,POLICY,Path(__file__)]},full_goal_complete=False))
    print('B218 retrospective13 five gates approved;one automatic wrap change/12exact stored retentions.No duplicate credit.Atomic registered integration pending.')
