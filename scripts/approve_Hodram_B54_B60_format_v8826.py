"""Approve82 source-bound formats with honest63-actual/19-offline scope;no credit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.review_Hodram_B54_B60_actual_v8825 import PROOFS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_format_v8826')
OLD=Path('translations/hodram_B54_B60_editorial_manuscript_v2.json')
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v3.json')
OLD_NAMES=Path('translations/hodram_B54_B60_speaker_name_review_v1.json')
NAMES=Path('translations/hodram_B54_B60_speaker_name_review_v2.json')
REVIEW=Path('work/analysis/Hodram_B54_B60_actual_review_v8825/qualified_actual_review.json')

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists() and not NAMES.exists()
    old,oldnames,review=map(read,[OLD,OLD_NAMES,REVIEW]);data={k:read(p) for k,p in PROOFS.items()}
    assert review['manuscript']['sha256']==sha(OLD.read_bytes()) and review['names']['sha256']==sha(OLD_NAMES.read_bytes())
    assert (review['total_runs'],review['total_frames'],review['total_holds'])==(14,130014,676)
    assert len(review['actual_unique_text_IDs'])==63 and len(review['offline_only_text_IDs'])==19 and review['all27_main_dialogue_transition_andfocused_transition_sheets_directly_viewed']
    assert data['independent']['whole_target_blocks_andarchive_byte_equal_to_sparse_rebuild'] and data['references']['external_references_complete']
    assert data['stored']['all82_complete_leading_internal_final_glyphs_independent_planes_bounds_consumption_andpagination_pass']
    assert data['relocation']['other318_blocks_byte_exact'] and data['relocation']['whole_inmemory_NDS_inverse_andall_other_files_components_exact']
    plan=read(old['compiled_plan']);assert not plan['failures']
    assert not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    doc,ng=deepcopy(old),deepcopy(oldnames);refs={r['id']:r for r in data['stored']['records']}
    for row in doc['records']:
        assert all(row['review'][g] is True for g in ['source','context','localization','naturalness']) and not row['review']['formatting']
        ref=refs[row['id']];assert row['source_reference']==ref['source_reference'] and row['current_reference']==ref['current_reference'] and row['compiled_hex']==ref['compiled_hex']
        actual=row['id'] in review['actual_unique_text_IDs'];FE=row['source_selector']==254
        reason=row['native_body_review_reason']+' Complete stored leading/internal/final glyphs, independent pixels, exact original six-byte preamble, full usable216px automatic wrapping, consumption, bounds and all expected native pages pass. '
        if actual:
            reason+='This utterance and every page were observed in paired initialized complete-script captures, with the original absent FE nameplate and transition preserved.' if FE else 'This utterance and every page, complete current progressive nameplate and original portrait were observed in paired initialized complete-script captures.'
        elif row['block']==55:
            reason+='This complete four-row guild message is offline-only. The same original progressive consumer, exact actor113 source/current getters/name plane and surname-macro expansion are bound; representative Port Worker and FA-macro behavior was observed elsewhere. This does not claim a new B55 visit.'
        else:
            reason+='This conditional B58 utterance remains offline-only. All source/current/target branches, native original voice/preamble, default macros and every stored page are bound; the complete unforced31-utterance path and the same consumer were observed. Sera andManuel headers anddelivery were also observed in B57/B60. No predicate,roster orplot flag is forced andthe conditional utterance is not relabeled actual coverage.'
        reason+=' Preserve all long/focused timing,RNG,RGB,calendar,actor andfollowing-command limits. No authored ordinary breaks,padding,shortening,narrowed viewport,altered font/metrics/guards,blank page orwaiver. No completion credit before registered integration.'
        row.update(final_reference=deepcopy(ref['final_reference']),stored_final_reference=deepcopy(ref['final_reference']),final_hex=ref['stored_hex'],stored_hex=ref['stored_hex'],
            compiler_owned_parity_space=ref['parity_space_added'],formatting_approval_reason=reason,formatting_registered_release_pending=True,
            actual_observation_status='paired-initialized-whole-script-every-page-observed' if actual else 'offline-only-sourcebound-mapped-native-pages-andrepresentative-consumer',
            formatting_gate_complete=True,current_review_status='all-five-individual-gates-reviewed-production-atomic-registered-pending')
        row['review']['formatting']=True
    observed=set(review['actual_progressive_actor_IDs'])
    for row in ng['records']:
        assert all(row['review'][g] is True for g in ['source','context','localization','naturalness']) and not row['review']['formatting']
        row['review']['formatting']=True;row['scoped_progressive_formatting_complete']=True;row['actual_scoped_progressive_header_observed']=row['actor_ID'] in observed
        row['formatting_approval_scope']='Exact source/current original progressive getters, fields, original voice/preamble consumers andcomplete native style11plane pass leading/internal/trailing glyphs andbounds in this batch\'s default captain1 context. '+('This exact progressive label was observed with complete name masks in paired initialized scenes.' if row['actor_ID'] in observed else 'This label is offline-only here;the same progressive name consumer was observed andsource/current fields remain unchanged. No new actual actor20 or113 header is claimed.')+' Full-catalogue UI,customnames,other contexts andthe complete207-entry editorial audit remain open;full-name Geronimo/Alonso shared de ownership is not approved by progressive formatting.'
    ng.update(predecessor_review=str(OLD_NAMES),predecessor_review_sha256=sha(OLD_NAMES.read_bytes()),all_individual_scoped_five_gates_true=True,
        scoped_progressive_formatting_complete=True,actual_progressive_actor_IDs=sorted(observed),offline_progressive_actor_IDs=[20,113],
        wider_catalogue_UI_all207_names_roles_aliases_customnames_andother_contexts_still_open=True,
        full_name_shared_de_ownership_deployment_andconsumers_still_open=True,formatting_actual_review=str(REVIEW),formatting_actual_review_sha256=sha(REVIEW.read_bytes()),new_credit=0,full_goal_complete=False)
    doc.update(encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),names_packet=str(NAMES),
        all_four_prose_gates_true_all_formatting_gates_false=False,all82_formatting_gates_still_false=False,
        all_five_individual_gates_true=True,source_current_final_references_complete=True,
        reference_ROM=data['reference']['research_ROM'],reference_ROM_sha256=data['reference']['research_ROM_sha256'],
        formatting_evidence={k:dict(path=p,sha256=sha(Path(p).read_bytes())) for k,p in PROOFS.items()},actual_review=str(REVIEW),actual_review_sha256=sha(REVIEW.read_bytes()),
        measured_limits=review,status='all-five-individual-gates-reviewed-production-atomic-registered-pending',
        remaining_required_work='Frozen source-qualified compiler/native policy andmeaningful changed-input guards,independent production evidence readers,whole-NDS atomic application,registered cumulative build/exactclean-input patch/ownstartup,then82once-only completion decisions. Full-name sharedde andall wider editorial scope remain open.',
        no_new_ROM_registered_stage_orcompletion_credit=True,new_credit=0,full_goal_complete=False)
    for before,after in zip(old['records'],doc['records'],strict=True):
        for key in ['id','english','logical_English','compiled_hex','source_hex','source_reference','current_hex','current_reference','decision','finding','localization_note','retention_reason','original_QA_issues']:
            assert before[key]==after[key]
    validate_natural_dialogue_batch(doc)
    ROOT.mkdir(parents=True);save(NAMES,ng);doc['names_packet_sha256']=sha(NAMES.read_bytes());save(DOC,doc)
    save(ROOT/'formatting_approval.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
        speech_approvals=82,scoped_progressive_name_approvals=10,all82_five_gates_true=True,standard_natural_dialogue_v2_validation_pass=True,
        all_source_current_final_references_words_compiledbytes_andindividual_prose_reasons_preserved=True,
        original_infos=sum(i['severity']=='info' for r in plan['records'] for i in r['base_QA']['issues']),warnings=0,waivers=0,
        offline_only_text_IDs=review['offline_only_text_IDs'],actual_unique_text_IDs=review['actual_unique_text_IDs'],measured_limits=review,
        complete_default_progressive_andFE_formatting_not_all207_fullcatalogue_UI_orcustomname_approval=True,
        production_atomic_registered_cleanpatch_startup_andcredit_pending=True,new_native_runs=0,new_emulator_runs=0,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [OLD,OLD_NAMES,REVIEW,*PROOFS.values(),Path(__file__)]}))
    print('Approved82 individual formats/10scoped progressive names;standardv2 pass.63actual/19offline,alllimits preserved.Production/atomic/registered integration andcredit pending.',flush=True)
