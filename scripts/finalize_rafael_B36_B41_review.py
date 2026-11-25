"""Close the existing 175 contextual reviews from scoped native and actual evidence."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B36_B41_checked_20261104')
FORMAT=Path('work/analysis/Rafael_B36_B41_formatting_20261104/speech_display_approved_v3')
DOC=Path('work/analysis/Rafael_B36_B41_formatting_20261104/formatting_input.json')
STORED=Path('work/analysis/Rafael_B36_B41_stored_native_20261104/stored_native_verification.json')
REBUILT=Path('work/analysis/Rafael_B36_B41_rebuilt_20261104/reconstruction.json')
NAMES=Path('work/analysis/Rafael_B36_B41_progressive_names_20261104/native_name_planes.json')
HEADERS=NAMES.with_name('actual_header_verification_v2.json')
PIXELS=Path('work/analysis/Rafael_B36_B41_focused_actual_pixels_20261104/focused_actual_pixels.json')
VISUAL=PIXELS.with_name('direct_visual_approval.json')
FINAL=Path('translations/rafael_B36_B41_contextual_final_review_v1.json')
NAME_FINAL=Path('translations/rafael_B36_B41_scoped_names_final_v1.json')
NEW_NAMES=Path('work/analysis/Rafael_B36_B41_new_name_bindings_20261104/names.json')

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists() and not NAME_FINAL.exists()
    doc,plan,native,display,stored,rebuilt,names,headers,pixels,visual=map(load,[DOC,FORMAT/'all175_compiled_plans.json',FORMAT/'all175_native_pages.json',
        FORMAT/'visual_approval.json',STORED,REBUILT,NAMES,HEADERS,PIXELS,VISUAL])
    assert len(doc['records'])==175 and (doc['proposed_revisions'],doc['wording_retentions'])==(76,99)
    assert native['all177_final_pages_directly_viewed'] and not native['direct_visual_review_pending']
    assert native['runtime']==stored['runtime'] and stored['complete_stored_pages']==display['pages']==177
    assert stored['fresh_relocated_native_relative_cases']==400 and stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert rebuilt['old_stored_native_sha256']==sha(STORED.read_bytes()) and rebuilt['stored_native_plane_andbranch_proofs_reused_on_exact_dependency_match']
    assert rebuilt['current_own_Rafael_runtime']==names['runtime'] and headers['native_names_sha256']==sha(NAMES.read_bytes())
    assert headers['all11_actors_observed'] and headers['complete_header_plane_comparisons']==40
    assert headers['six_new_native_name_previews_directly_viewed'] and visual['all_three_sheets_directly_viewed']
    assert pixels['all_selected_pages_observed_in_exact_fixture_order'] and (pixels['selected_utterances'],pixels['selected_pages'],pixels['complete_body_planes'])==(16,18,40)
    old_names_path=Path('translations/rafael_B42_B43_scoped_names_final_v1.json');old_names=load(old_names_path)
    newer=load(NEW_NAMES);source={r['actor_ID']:r for r in newer['clean_names']['rows'] if r['consumer']=='progressive-nameplate'}
    reasons={8:'Retain Arcadius Eudoxios, matching the complete clean progressive name and established character identity. The additional catalogue middle component is separate; no gender or title is inferred.',
        31:'Retain Pedro Valdes in progressive dialogue, matching the clean Pedro/Valdes components. The separate catalogue de correction does not change this nameplate.',
        34:'Retain the established Barbarossa Hayreddin, matching the clean progressive identity. Add no Lord or pirate-king rank; the separate Fazul catalogue glyph proposal is not deployed here.',
        51:'Retain Salid Ajar, matching source サリド・アジャール and the native nameplate. Dialogue uses Salid consistently rather than the earlier Salih spelling.',
        75:'Retain the established Hans Letzel spelling consistently with the previously reviewed ruins/Proof dialogue; the source names the same character, without adding a title.',
        151:'Retain Sailor for source 水夫 in the lookout exchange. The unused catalogue 配下/Retainer component supplies no new nationality,rank or biography.',
        153:'Retain Sailor for source 水夫 answering the fleet order. Keep the role natural and consistent with the other sailor; do not substitute unused Retainer metadata or add cultural labels.'}
    name_records=deepcopy(old_names['records'])
    for row in name_records:row['context']='Same recurring companion in complete Rafael B36–B41 exchanges; retain the previously approved identity.'
    for consumer in names['consumer_bindings']:
        actor=consumer['actor_ID']
        if actor not in source:continue
        src=source[actor];reason=reasons[actor]
        name_records.append(dict(id=f'RAFAEL_B36_B41_ACTOR_{actor}',actor_ID=actor,english=consumer['text'],speaker=consumer['text'],source_meaning=src['text'],
            context='Scoped progressive speaker identity in the complete Rafael pirate/Spanish/Dutch/ruins exchanges; source role and dialogue context considered together.',
            localization_note=reason,decision='retention',retention_reason=reason,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=True),
            source_reference=dict(native_binding=str(NEW_NAMES),native_binding_sha256=sha(NEW_NAMES.read_bytes()),actor_ID=actor,consumer='progressive-nameplate',text_hex=src['text_hex']),
            current_reference=dict(native_binding=str(NAMES),native_binding_sha256=sha(NAMES.read_bytes()),actor_ID=actor,consumer='progressive-nameplate',text_hex=consumer['text_hex']),
            full_catalogue_UI_unvisited=True,progressive_consumer_only=True))
    assert len(name_records)==11
    names_final=dict(format='dk4-scoped-progressive-name-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],records=name_records,no_name_data_change=True,no_new_dialogue_credit=True,
        progressive_consumers_only=True,full_catalogue_UI_unvisited=True,two_catalogue_field_corrections_pending=True,formatting_evidence=str(HEADERS),global_207_name_review_still_open=True)
    validate_natural_dialogue_batch(names_final)
    ROOT.mkdir();save(NAME_FINAL,names_final)
    actual=dict(total_frames=10001,initialized_fixture_runs=1,actual_utterances=16,actual_pages=18,offline_only_utterances=159,
        complete_body_planes=40,complete_name_header_planes=40,observed_actor_IDs=sorted(r['actor_ID'] for r in name_records),
        all_three_QA_sheets_directly_viewed=True,all_required_distinct_wrap_glyph_macro_pagination_cases_pass=True,
        read_only_pixel_proof=str(PIXELS),read_only_pixel_proof_sha256=sha(PIXELS.read_bytes()),header_proof=str(HEADERS),header_proof_sha256=sha(HEADERS.read_bytes()),
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,disclosed_synthetic_display_sequence=True,new_credit=0,guide_photos=False)
    save(ROOT/'actual_review.json',actual)
    bystored={r['id']:r for r in stored['records']};byplan={r['id']:r for r in plan['records']}
    final=deepcopy(doc)
    for row in final['records']:
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        entry=bystored[row['id']];row['review']['formatting']=True
        row['planned_English_markup']=byplan[row['id']]['English']
        row['planned_integrated_reference']=dict(file_path=doc['file_path'],block=row['block'],offset=entry['new_offset'],header_offset=entry['new_offset']-5,
            record_index=entry['new_record_index'],exact_stored_hex=entry['stored_hex'],target_archive_sha256=rebuilt['target_archive_sha256'])
        row.update(registered_release_andcompletion_credit_pending=True,formatting_evidence=dict(native=str(FORMAT/'all175_native_pages.json'),stored=str(STORED),
            representative_actual=str(ROOT/'actual_review.json'),scope='All177 pages checked offline;16 utterances observed in a disclosed display fixture,159 offline-only.'))
    final.update(format='dk4-editorial-final-review-v1',all_five_individual_review_gates_passed=True,all_formatting_gates_false=False,
        all_fifth_formatting_gates_still_pending=False,scoped_name_review=str(NAME_FINAL),scoped_name_review_sha256=sha(NAME_FINAL.read_bytes()),
        registered_release_andcompletion_credit_pending=True,new_credit=0,
        formatting_evidence={str(p):sha(p.read_bytes()) for p in [FORMAT/'all175_compiled_plans.json',FORMAT/'all175_native_pages.json',FORMAT/'visual_approval.json',
            STORED,REBUILT,NAMES,HEADERS,PIXELS,VISUAL,NAME_FINAL,ROOT/'actual_review.json',Path(__file__)]})
    validate_natural_dialogue_batch(final);save(FINAL,final);save(ROOT/'release_plans.json',plan)
    save(ROOT/'formatting_checkpoint.json',dict(final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),scoped_names=str(NAME_FINAL),
        scoped_names_sha256=sha(NAME_FINAL.read_bytes()),prose_reviews=175,revised=76,retained=99,pages=177,layout_corrections=4,ASCII_I_fixes=2,
        scoped_names_retained=11,actual_frames=10001,actual_utterances=16,actual_pages=18,offline_only_utterances=159,actual_body_planes=40,actual_header_planes=40,
        all_individual_five_gates_pass_in_research=True,registered_release_andcompletion_credit_pending=True,new_credit=0,guide_photos=False,full_goal_complete=False))
    print('175 five-gate research reviews/76 revisions/99 retentions and11 scoped name retentions sealed;registered integration pending,zero credit.')
