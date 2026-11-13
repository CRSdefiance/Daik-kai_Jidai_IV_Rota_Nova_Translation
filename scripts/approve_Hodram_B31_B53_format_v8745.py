"""Approve complete source/native/stored formats with representative actual scope."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.review_Hodram_B31_B53_actual_v8744 import PROOFS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_format_v8745')
OLD=Path('translations/hodram_B31_B53_editorial_manuscript_v3.json')
DOC=Path('translations/hodram_B31_B53_editorial_manuscript_v4.json')
OLD_NAMES=Path('translations/hodram_B31_B53_speaker_name_review_v2.json')
NAMES=Path('translations/hodram_B31_B53_speaker_name_review_v3.json')
REVIEW=Path('work/analysis/Hodram_B31_B53_actual_review_v8744/qualified_actual_review.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists() and not NAMES.exists()
    old,oldnames,review=map(read,[OLD,OLD_NAMES,REVIEW]);data={k:read(p) for k,p in PROOFS.items()}
    assert review['manuscript']['sha256']==sha(OLD.read_bytes()) and review['names']['sha256']==sha(OLD_NAMES.read_bytes())
    assert (review['total_runs'],review['total_frames'],review['total_holds'])==(4,24004,76)
    assert review['offline_only_text_IDs']==['DK4_MES_B31_R0013'] and review['all_four_sheets_directly_viewed']
    assert not data['plan']['failures'] and all(not r['base_QA']['issues'] for r in data['plan']['records'])
    assert data['references']['external_references_complete'] and data['independent']['whole_target_blocks_andarchive_byte_equal_to_sparse_rebuild']
    assert data['stored']['complete3stored_first_internal_final_glyphs_independent_planes_bounds_consumption_andpagination_pass']
    assert data['relocation']['other323_blocks_byte_exact'] and data['relocation']['whole_inmemory_NDS_inverse_andall_other_files_components_exact']
    doc,ng=deepcopy(old),deepcopy(oldnames);refs={r['id']:r for r in data['stored']['records']}
    for row in doc['records']:
        assert all(row['review'][g] is True for g in ['source','context','localization','naturalness']) and not row['review']['formatting']
        ref=refs[row['id']];assert row['source_reference']==ref['source_reference'] and row['current_reference']==ref['current_reference'] and row['compiled_hex']==ref['compiled_hex']
        actual=row['id'] in review['actual_unique_text_IDs']
        reason=row['native_body_review_reason']+' Complete stored first/internal/final glyphs, original six-byte preamble, automatic full216px wrapping, exact consumption/bounds/single-page pagination and source/current/final references pass. '
        reason+=('This exact utterance and its complete current progressive nameplate/portrait were observed in paired initialized Japanese/English complete-script captures.' if actual else
            'This shorter B31 variant remains offline-only. Both source/current relative paths and the complete short stored page are bound natively; the longer variant with the identical original actor34 preamble and the same progressive consumer was observed in both languages. Representative coverage does not require forcing the original query or claiming an unvisited branch.')
        reason+=' No authored ordinary break, padding, shortening, narrowed viewport, altered font/metrics/guard, extra page or waiver. No new source-prose orcompletion credit before registered integration.'
        historical={}
        for field in ['source_presentation_consumer_not_yet_approved','source_meaning_only_not_editorial_orformatting_approval','native_branch_membership_androle_name_full_preamble_consumer_pending']:
            if row.get(field) is True:historical[field]=True;row[field]=False
        row.update(final_reference=deepcopy(ref['final_reference']),stored_final_reference=deepcopy(ref['final_reference']),final_hex=ref['stored_hex'],stored_hex=ref['stored_hex'],
            compiler_owned_parity_space=ref['parity_space_added'],formatting_approval_reason=reason,formatting_registered_release_pending=True,
            actual_observation_status='paired-whole-script-body-name-andportrait-observed' if actual else 'offline-only-unforced-short-variant-withrepresentative-sameconsumer-longvariant',
            historical_preformat_pending_flags=historical,current_review_status='all-five-individual-gates-reviewed-frozen-policy-production-atomic-registered-pending')
        row['review']['formatting']=True
    assert len(ng['records'])==2 and [r['actor_ID'] for r in ng['records']]==[34,113]
    for row in ng['records']:
        assert all(row['review'][g] is True for g in ['source','context','localization','naturalness']) and not row['review']['formatting']
        row['review']['formatting']=True
        row['formatting_approval_scope']='Complete unchanged current progressive nameplate and portrait, exact source/current fields and original getters/native glyph plane,38 paired actual complete holds for this actor across Japanese/English fixtures. Source full-getter composition and literal planes reviewed for actor34; no actual full-catalogue UI, wider-context,customname orfull207 approval.'
        row['actual_scene_header_andfinal_formatting_pending']=False
        if row['actor_ID']==113:row['actual_B53_header_observation_pending']=False
        if row['actor_ID']==34:
            resolution=row['full_name_resolution'];resolution['prior_combined_unobserved_flag']=resolution['actual_B31_progressive_header_andrelevant_catalogue_UI_coverage_still_unobserved']
            resolution['actual_B31_progressive_header_andrelevant_catalogue_UI_coverage_still_unobserved']=False
            resolution['actual_B31_progressive_header_verified']=True;resolution['full_catalogue_UI_still_unobserved']=True
    ng['full_name_resolution']=deepcopy(ng['records'][0]['full_name_resolution'])
    ng.update(predecessor_review=str(OLD_NAMES),predecessor_review_sha256=sha(OLD_NAMES.read_bytes()),actual_headers_formatting_andwider_catalogue_UI_pending=False,
        scoped_progressive_headers_andformatting_complete=True,wider_catalogue_UI_all207_names_roles_aliases_customnames_andother_contexts_still_open=True,
        all_individual_scoped_five_gates_true=True,formatting_actual_review=str(REVIEW),formatting_actual_review_sha256=sha(REVIEW.read_bytes()),new_credit=0,full_goal_complete=False)
    doc.update(encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),names_packet=str(NAMES),
        all_four_prose_gates_true_all_formatting_gates_false=False,all_three_formatting_gates_still_false=False,
        all_five_individual_gates_true=True,source_current_final_references_complete=True,
        reference_ROM=data['reference']['research_ROM'],reference_ROM_sha256=data['reference']['research_ROM_sha256'],
        formatting_evidence={k:dict(path=p,sha256=sha(Path(p).read_bytes())) for k,p in PROOFS.items()},
        actual_review=str(REVIEW),actual_review_sha256=sha(REVIEW.read_bytes()),measured_limits=review,
        status='all-five-individual-gates-reviewed-frozen-policy-production-atomic-registered-pending',
        remaining_required_work='Frozen source-qualified compiler/native policy and meaningful changed-input checks, independent production evidence readers, one whole-NDS atomic commit, shared registered cumulative release/exact clean-input patch/own startup, then exactly three once-only completion decisions.',
        no_new_ROM_registered_stage_orcompletion_credit=True,new_credit=0,full_goal_complete=False)
    for before,after in zip(old['records'],doc['records'],strict=True):
        for key in ['id','english','logical_English','compiled_hex','source_hex','source_reference','current_hex','current_reference','decision','finding','localization_note']:
            assert before[key]==after[key]
    validate_natural_dialogue_batch(doc)
    ROOT.mkdir(parents=True);save(NAMES,ng);doc['names_packet_sha256']=sha(NAMES.read_bytes());save(DOC,doc)
    save(ROOT/'formatting_approval.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
        speech_approvals=3,scoped_progressive_name_approvals=2,all3_five_gates_true=True,standard_natural_dialogue_v2_validation_pass=True,
        all_source_current_final_references_words_compiledbytes_andindividual_prose_reasons_preserved=True,
        original_infos=0,warnings=0,waivers=0,offline_only_text_IDs=['DK4_MES_B31_R0013'],
        actual_unique_text_IDs=review['actual_unique_text_IDs'],measured_limits=review,
        source_name_fullgetter_composition_andretention_not_fullcatalogue_UI_approval=True,
        frozen_policy_production_atomic_registered_patch_startup_andcredit_pending=True,new_native_runs=0,new_emulator_runs=0,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [OLD,OLD_NAMES,REVIEW,*PROOFS.values(),Path(__file__)]}))
    print('Approved3individual speech formats/2scoped current headers;standardv2 pass. Actual B31long/B53warning,short offline;allwords/bytes/refs exact. Formal production/registered integration andcredit remain pending.',flush=True)
